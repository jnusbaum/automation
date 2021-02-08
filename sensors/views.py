from django.conf import settings
from django.shortcuts import render

from sensors.models import *


def dashboard(request):
    return render(request, 'sensors/sensors-dashboard.html')

def all_sensors(request):
    pass

def overlay(request):
    pass

def test(request):
    pass

def sensor(request):
    pass





