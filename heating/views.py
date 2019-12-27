from django.http import HttpResponse
from django.shortcuts import render
import requests
from decimal import *
from datetime import datetime
from statistics import mean

host = 'http://192.168.0.134/dataserver'

zones = ('MBR', 'MBATH', 'LIBRARY', 'KITCHEN', 'LAUNDRY', 'GARAGE', 'FAMILY', 'OFFICE', 'EXERCISE', 'GUEST', 'VALVE', 'BOILER')

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
    # first get sensors
    r = requests.get(f'{host}/sensors')
    if requests.codes.ok != r.status_code:
        # error
        return HttpResponse(status=r.status_code)
    data = r.json()
    sensors = data['data']
    sensors.sort(key=lambda x: x['id'])
    samples = {}
    for sensor in sensors:
        r = requests.get(f"{host}/sensors/{sensor['id']}/data")
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
    return render(request, 'heating/heating-dashboard.html', {'zones': zones, 'samples': samples})


def zone(request, zone_name):
    return render(request, 'heating/heating-zone.html', {'zone': zone_name, 'zones': zones})


def view_all(request):
    # get data for all zones
    datapts = request.GET.get('datapts', '100')
    targettime = request.GET.get('targettime', datetime_to_str(datetime.today()))
    # look for zone names
    dzones = []
    if 'ALL' in request.GET:
        dzones = zones
    else:
        for zone in zones:
            if zone in request.GET:
                dzones.append(zone)

    # input, will return latest value
    params = {'datapts': datapts, 'targettime': targettime}
    samples = {}
    for zone_name in dzones:
        if zone_name == 'VALVE':
            r = requests.get(f'{host}/sensors/{zone_name}-INSYS/data', params=params)
        else:
            r = requests.get(f'{host}/sensors/{zone_name}-IN/data', params=params)
        if requests.codes.ok != r.status_code:
            # error
            return HttpResponse(status=r.status_code)
        data = r.json()
        invals = data
        # output
        r = requests.get(f'{host}/sensors/{zone_name}-OUT/data', params=params)
        if requests.codes.ok != r.status_code:
            # error
            return HttpResponse(status=r.status_code)
        data = r.json()
        outvals = data
        # join data
        sdata = [(str_to_datetime(invals['data'][i]['attributes']['timestamp']),
                  Decimal(invals['data'][i]['attributes']['value_real']),
                  Decimal(outvals['data'][i]['attributes']['value_real'])) for i in range(0, invals['count'])]
        samples[zone_name] = sdata

    return render(request, 'heating/heating-all.html', {'datapts': datapts, 'zones': zones, 'samples': samples})
