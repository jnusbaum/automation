from django.http import HttpResponse
from django.shortcuts import render
import requests
from decimal import *
from datetime import datetime

host = 'http://192.168.0.134'

def str_to_datetime(ans):
    if ans:
        d = datetime.strptime(ans, "%Y-%m-%d-%H-%M-%S")
        # no tz info, assumed to be in UTC
        return d
    return None


def index(request):
    # fake samples
    # samples = [
    #     {'name': 'MBR-IN', 'timestamp': '2019-12-12-14-22-34', 'value': '142.45'},
    #     {'name': 'MBR-OUT', 'timestamp': '2019-12-12-14-22-34', 'value': '102.00'},
    #     {'name': 'OFFICE-IN', 'timestamp': '2019-12-12-14-22-34', 'value': '94.50'},
    #     {'name': 'OFFICE-OUT', 'timestamp': '2019-12-12-14-22-34', 'value': '92.67'},
    # ]
    # get samples from data server
    # first get sensors
    r = requests.get(f'{host}/sensors')
    if requests.codes.ok != r.status_code:
        # error
        return HttpResponse(status_code=r.status_code)
    data = r.json()
    sensors = data['data']
    sensors.sort(key=lambda x: x['id'])
    samples = {}
    for sensor in sensors:
        r = requests.get(f"{host}/sensors/{sensor['id']}/data")
        if requests.codes.ok != r.status_code:
            # error
            return HttpResponse(status_code=r.status_code)
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
            samples[sensor['id'].replace('-', '_')] = {'name': sensor['id'], 'timestamp': sample['attributes']['timestamp'], 'value': sample['attributes']['value_real'], 'dclass': dclass}
    return render(request, 'heating/heating-dashboard.html', {'samples': samples})


def clean_data(sdata):
    outdata = []
    # if x more than 25% diif from x-1
    # then x = x-1
    prev_in = sdata[0][1]
    prev_out = sdata[0][2]
    badin = 0
    badout = 0
    for item in sdata:
        timestamp = item[0]
        if abs(item[1] - prev_in) / prev_in < .25:
            inval = item[1]
        else:
            inval = prev_in
            badin += 1
        prev_in = inval
        if abs(item[2] - prev_out) / prev_out < .25:
            outval = item[2]
        else:
            outval = prev_out
            badout += 1
        prev_out = outval
        outdata.append((timestamp, inval, outval))
    return outdata, badin, badout



def zone(request, zone_name):
    # get data for zone
    # input, will return latest value
    params = {'datapts': 9000}
    if zone_name == 'VALVE':
        r = requests.get(f'{host}/sensors/{zone_name}-INSYS/data', params=params)
    else:
        r = requests.get(f'{host}/sensors/{zone_name}-IN/data', params=params)
    if requests.codes.ok != r.status_code:
        # error
        return HttpResponse(status_code=r.status_code)
    data = r.json()
    invals = data
    # output
    r = requests.get(f'{host}/sensors/{zone_name}-OUT/data', params=params)
    if requests.codes.ok != r.status_code:
        # error
        return HttpResponse(status_code=r.status_code)
    data = r.json()
    outvals = data
    # join data
    sdata = [(str_to_datetime(invals['data'][i]['attributes']['timestamp']),
              Decimal(invals['data'][i]['attributes']['value_real']),
              Decimal(outvals['data'][i]['attributes']['value_real'])) for i in range(0, invals['count'])]
    sdata, badin, badout = clean_data(sdata)
    samples = {'data': sdata, 'badin': badin, 'badout': badout, 'zone': zone_name }

    return render(request, 'heating/heating-zone.html', {'samples': samples})
