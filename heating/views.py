from django.conf import settings
from django.shortcuts import render

from heating.models import *


def dashboard(request):
    zones = Zone.objects.all().order_by('name')
    return render(request, 'heating/heating-dashboard.html', {'host': settings.DATASERVER_HOST, 'zones': zones})


def zone(request, zone_name):
    zones = Zone.objects.all().order_by('name')
    if zone_name in ('BOILER', 'WHEAT1', 'WHEAT2'):
        return render(request, 'heating/heating-zone-wburn.html',
                      {'host': settings.DATASERVER_HOST, 'zone': zone_name, 'zones': zones})
    else:
        return render(request, 'heating/heating-zone.html',
                      {'host': settings.DATASERVER_HOST, 'zone': zone_name, 'zones': zones})


def all_zones(request):
    # get data for all zones
    datapts = int(request.GET.get('datapts', '24'))
    zones = Zone.objects.all().order_by('name')
    dzones = []
    if 'ALL' in request.GET:
        dzones = zones
    else:
        for z in zones:
            if z.name in request.GET:
                dzones.append(z)

    return render(request, 'heating/heating-all.html', {'host': settings.DATASERVER_HOST + "/heating/api",
                                                        'datapts': datapts,
                                                        'allzones': zones,
                                                        'zones': dzones})


def overlay(request):
    # get data for all zones
    datapts = request.GET.get('datapts', '24')
    zones = Zone.objects.all().order_by('name')
    dzones = []
    if 'ALL' in request.GET:
        dzones = zones
    else:
        for z in zones:
            if z.name in request.GET:
                dzones.append(z)
    osensors = []
    for z in dzones:
        for sensor in z.tempsensor_set.all():
            osensors.append(sensor)
    return render(request, 'heating/heating-overlay.html', {'host': settings.DATASERVER_HOST + "/heating/api",
                                                            'datapts': datapts,
                                                            'allzones': zones,
                                                            'zones': dzones,
                                                            'sensors': osensors})


def test(request, zone_name):
    return render(request, 'heating/heating-test.html', {'host': settings.DATASERVER_HOST + "/heating/api",
                                                         'zone': zone_name})
