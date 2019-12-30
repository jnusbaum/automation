from django.http import HttpResponse
from django.shortcuts import render
import requests
from decimal import *
from datetime import datetime

from django.conf import settings


def str_to_datetime(ans):
    if ans:
        d = datetime.strptime(ans, "%Y-%m-%d-%H-%M-%S")
        return d
    return None


def datetime_to_str(ans):
    if ans:
        d = ans.strftime("%Y-%m-%d-%H-%M-%S")
        return d
    return None


def index(request):
    # get samples from data server
    r = requests.get(f'{settings.DATASERVER_HOST}/zones')
    if requests.codes.ok != r.status_code:
        # error
        return HttpResponse(status=r.status_code)
    data = r.json()
    zones = data['data']
    zones.sort(key=lambda x: x['id'])
    # first get sensors
    r = requests.get(f'{settings.DATASERVER_HOST}/sensors')
    if requests.codes.ok != r.status_code:
        # error
        return HttpResponse(status=r.status_code)
    data = r.json()
    sensors = data['data']
    sensors.sort(key=lambda x: x['id'])
    samples = {}
    for sensor in sensors:
        r = requests.get(f"{settings.DATASERVER_HOST}/sensors/{sensor['id']}/data")
        if requests.codes.ok != r.status_code:
            # error
            return HttpResponse(status=r.status_code)
        data = r.json()
        for sample in data['data']:
            dval = Decimal(sample['attributes']['value_real'])
            if dval < 70:
                dclass = 'cold'
            elif dval < 90:
                dclass = 'cool'
            elif dval < 110:
                dclass = 'luke-warm'
            elif dval < 130:
                dclass = 'warm'
            elif dval < 150:
                dclass = 'very-warm'
            else:
                dclass = 'hot'
            samples[sensor['id'].replace('-', '_')] = {'name': sensor['id'],
                                                       'timestamp': sample['attributes']['timestamp'],
                                                       'value': sample['attributes']['value_real'],
                                                       'dclass': dclass}
    return render(request, 'heating/heating-dashboard.html', {'host': settings.DATASERVER_HOST, 'zones': zones, 'samples': samples})


def zone(request, zone_name):
    r = requests.get(f'{settings.DATASERVER_HOST}/zones')
    if requests.codes.ok != r.status_code:
        # error
        return HttpResponse(status=r.status_code)
    data = r.json()
    zones = data['data']
    zones.sort(key=lambda x: x['id'])
    return render(request, 'heating/heating-zone.html', {'host': settings.DATASERVER_HOST, 'zone': zone_name, 'zones': zones})


def view_all(request):
    # get data for all zones
    datapts = request.GET.get('datapts', '100')
    targettime = request.GET.get('targettime', datetime_to_str(datetime.today()))
    # look for zone names
    r = requests.get(f'{settings.DATASERVER_HOST}/zones')
    if requests.codes.ok != r.status_code:
        # error
        return HttpResponse(status=r.status_code)
    data = r.json()
    zones = data['data']
    zones.sort(key=lambda x: x['id'])
    dzones = []
    if 'ALL' in request.GET:
        dzones = zones
    else:
        for zone in zones:
            if zone['id'] in request.GET:
                dzones.append(zone)

    # input, will return latest value
    params = {'datapts': datapts, 'targettime': targettime}
    samples = {}
    for zone in dzones:
        zone_name = zone['id']
        r = requests.get(f'{settings.DATASERVER_HOST}/zones/{zone_name}/data', params=params)
        if requests.codes.ok != r.status_code:
            # error
            return HttpResponse(status=r.status_code)
        data = r.json()
        data = data['data']
        count = None
        invals = []
        outvals = []
        for sensor_name, sdata in data.items():
            if count:
                if sdata['count'] != count:
                    # unequal length time series
                    return HttpResponse(status=500)
            else:
                count = sdata['count']
            if sensor_name.endswith('-IN') or sensor_name.endswith('-INSYS'):
                invals = sdata['data']
            elif sensor_name.endswith('-OUT'):
                outvals = sdata['data']
        sdata = [(str_to_datetime(invals[i]['attributes']['timestamp']),
                  Decimal(invals[i]['attributes']['value_real']),
                  Decimal(outvals[i]['attributes']['value_real'])) for i in range(0, len(invals))]
        samples[zone_name] = sdata

    return render(request, 'heating/heating-all.html', {'host': settings.DATASERVER_HOST,
                                                        'datapts': datapts,
                                                        'zones': zones,
                                                        'samples': samples})
