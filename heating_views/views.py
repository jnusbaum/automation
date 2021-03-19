from django.conf import settings
from django.shortcuts import render

from heating.models import *


def dashboard(request):
    zones = Zone.objects.all().order_by('name')
    boilers = Boiler.objects.all().order_by('name')
    valves = MixingValve.objects.all().order_by('name')
    return render(request, 'heating/heating-dashboard.html', {'host': settings.DATASERVER_HOST,
                                                              'zones': [z.name for z in zones],
                                                              'boilers': [b.name for b in boilers],
                                                              'valves': [v.name for v in valves],
                                                              })


def zone(request, zone_name):
    zones = Zone.objects.all().order_by('name')
    return render(request, 'heating/heating-zone.html',
                    {'host': settings.DATASERVER_HOST, 'zone': zone_name, 'zones': zones})


def boiler(request, boiler_name):
    boilers = Boiler.objects.all().order_by('name')
    return render(request, 'heating/heating-boiler.html',
                    {'host': settings.DATASERVER_HOST, 'boiler': boiler_name, 'boilers': boilers})


def mixingvalve(request, valve_name):
    mixingvalves = MixingValve.objects.all().order_by('name')
    return render(request, 'heating/heating-mixingvalve.html',
                    {'host': settings.DATASERVER_HOST, 'mixingvalve': valve_name, 'mixingvalves': mixingvalves})


def all_zones(request):
    zones = Zone.objects.all().order_by('name')
    boilers = Boiler.objects.all().order_by('name')
    valves = MixingValve.objects.all().order_by('name')
    return render(request, 'heating/heating-all.html', {'host': settings.DATASERVER_HOST,
                                                              'zones': [z.name for z in zones],
                                                              'boilers': [b.name for b in boilers],
                                                              'valves': [v.name for v in valves],
                                                              })


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
        for sensor in z.sensors.all():
            osensors.append(sensor)
    return render(request, 'heating/heating-overlay.html', {'host': settings.DATASERVER_HOST,
                                                            'datapts': datapts,
                                                            'allzones': zones,
                                                            'zones': dzones,
                                                            'devices': osensors})


def test(request, zone_name):
    return render(request, 'heating/heating-test.html', {'host': settings.DATASERVER_HOST,
                                                         'zone': zone_name})


