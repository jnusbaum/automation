from . import settings
from django.shortcuts import render


def dashboard(request):
    pass


def test_heater(request, heater_name):
    return render(request, 'hotwater/hotwater-waterheater.html', {'host': settings.DATASERVER_HOST,
                                                                  'heater': heater_name})

def test_pump(request, pump_name):
    return render(request, 'hotwater/hotwater-circpump.html', {'host': settings.DATASERVER_HOST,
                                                                  'pump': pump_name})

def test_spinner(request):
    return render(request, 'hotwater/spinner-test.html')
