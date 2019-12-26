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
    return render(request, 'heating/heating-dashboard.html', {'samples': samples})


def clean_data(sdata):
    outdata1 = []
    badin = 0
    badout = 0
    # first pass remove all less than 0 and 77 (seems to be a special "error" value)
    for data in sdata:
        if data[1] < 0 or data[1] == 77:
            badin += 1
        elif data[2] < 0 or data[2] == 77:
            badout += 1
        else:
            outdata1.append(data)

    outdata2 = []
    # 3 point window, x, y, z
    # avgxz = average of x and z
    # diffy = abs(y - avgxz)
    # if diffy > 35% replace y with avgxz
    # also look for less than 0 and
    xi = outdata1[0][1]
    yi = outdata1[1][1]
    zi = outdata1[2][1]
    xo = outdata1[0][2]
    yo = outdata1[1][2]
    zo = outdata1[2][2]
    outdata2.append((outdata1[0][0], outdata1[0][1], outdata1[0][2]))
    ty = outdata1[1][0]
    for i in range(3, len(outdata1)):
        inval = 0
        outval = 0

        avgxz = mean((xi, zi))
        if yi > 0:
            diffy = abs(yi - avgxz)/avgxz
            if diffy > .35:
                inval = avgxz  # set current item to avg
                badin += 1
            else:
                inval = yi
        else:
            inval = avgxz
            badin += 1

        xi = inval
        yi = zi
        zi = outdata1[i][1]

        avgxz = mean((xo, zo))
        if yo > 0:
            diffy = abs(yo - avgxz)/avgxz
            if diffy > .35:
                outval = avgxz  # set current item to avg
                badout += 1
            else:
                outval = yo
        else:
            outval = avgxz
            badout += 1

        xo = outval
        yo = zo
        zo = outdata1[i][2]
        outdata2.append((ty, inval, outval))
        ty = outdata1[i-1][0]

    inval = 0
    outval = 0

    avgxz = mean((xi, zi))
    if yi > 0:
        diffy = abs(yi - avgxz)/avgxz
        if diffy > .35:
            inval = avgxz  # set current item to avg
            badin += 1
        else:
            inval = yi
    else:
        inval = avgxz
        badin += 1

    yi = zi

    avgxz = mean((xo, zo))
    if yo > 0:
        diffy = abs(yo - avgxz)/avgxz
        if diffy > .35:
            outval = avgxz  # set current item to avg
            badout += 1
        else:
            outval = yo
    else:
        outval = avgxz
        badout += 1

    yo = zo

    outdata2.append((ty, inval, outval))
    ty = outdata1[i][0]
    outdata2.append((ty, yi, yo))

    return outdata2, badin, badout


def zone(request, zone_name):
    samples = {'zone': zone_name }
    return render(request, 'heating/heating-zone.html', {'samples': samples})


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
        sdata, badin, badout = clean_data(sdata)
        samples[zone_name] = sdata

    return render(request, 'heating/heating-all.html', {'datapts': datapts, 'samples': samples})
