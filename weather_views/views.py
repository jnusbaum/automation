from django.conf import settings
from django.shortcuts import render

from weather.models import *


def dashboard(request):
    sensors = Weather.objects.all().order_by('name')
    return render(request, 'weather_views/weather-dashboard.html', {'host': settings.DATASERVER_HOST,
                                                                    'hours': 24,
                                                                    'sensors': [s.name for s in sensors],
                                                                    })


def sensor(request, sensor_name):
    sensors = Weather.objects.all().order_by('name')
    return render(request, 'weather_views/weather.html',
                  {'host': settings.DATASERVER_HOST, 'hours': 24, 'sensor': sensor_name, 'sensors': sensors})

