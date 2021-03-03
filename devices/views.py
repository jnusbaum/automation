from django.conf import settings
from django.shortcuts import render
from devices.models import *


def dashboard(request):
    sensors = TempSensor.objects.all().order_by('name')
    return render(request, 'devices/devices-dashboard.html', {'host': settings.DATASERVER_HOST,
                                                              'sensors': [s.name for s in sensors],
                                                              })
    return render(request, 'devices/devices-dashboard.html')


def all_sensors(request):
    pass


def overlay(request):
    pass


def test(request):
    pass


def sensor(request):
    pass
