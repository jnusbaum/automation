from django.conf import settings
from django.shortcuts import render

from heating.models import *


def dashboard(request):
    zones = Zone.objects.all().order_by('name')
    boilers = Boiler.objects.all().order_by('name')
    valves = MixingValve.objects.all().order_by('name')
    return render(request, 'heating_views/heating-dashboard.html', {'host': settings.DATASERVER_HOST,
                                                                    'hours': 24,
                                                              'zones': [z.name for z in zones],
                                                              'boilers': [b.name for b in boilers],
                                                              'valves': [v.name for v in valves],
                                                              })


def zone(request, zone_name):
    zones = Zone.objects.all().order_by('name')
    return render(request, 'heating_views/heating-zone.html',
                    {'host': settings.DATASERVER_HOST, 'hours': 24, 'zone': zone_name, 'zones': zones})


def boiler(request, boiler_name):
    boilers = Boiler.objects.all().order_by('name')
    return render(request, 'heating_views/heating-boiler.html',
                    {'host': settings.DATASERVER_HOST, 'hours': 24, 'boiler': boiler_name, 'boilers': boilers})


def mixingvalve(request, valve_name):
    mixingvalves = MixingValve.objects.all().order_by('name')
    return render(request, 'heating_views/heating-mixingvalve.html',
                    {'host': settings.DATASERVER_HOST, 'hours': 24, 'mixingvalve': valve_name, 'mixingvalves': mixingvalves})
