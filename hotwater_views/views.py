from . import settings
from django.shortcuts import render
from hotwater.models import *


def dashboard(request):
    # get list of water heaters and circulation pumps
    heaters = WaterHeater.objects.all().order_by('name')
    pumps = CircPump.objects.all().order_by('name')
    return render(request, 'hotwater_views/hotwater-dashboard.html', {'host': settings.DATASERVER_HOST,
                                                                      'hours': 24,
                                                                'heaters': [h.name for h in heaters],
                                                                'pumps': [p.name for p in pumps]})


def heater(request, heater_name):
    return render(request, 'hotwater_views/hotwater-waterheater.html', {'host': settings.DATASERVER_HOST,
                                                                        'hours': 24,
                                                                        'heater': heater_name})

def pump(request, pump_name):
    return render(request, 'hotwater_views/hotwater-circpump.html', {'host': settings.DATASERVER_HOST,
                                                                     'hours': 24,
                                                                    'pump': pump_name})

