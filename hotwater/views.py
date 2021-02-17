from . import settings
from django.shortcuts import render


def dashboard(request):
    pass


def test_heater(request, heater_name):
    return render(request, 'hotwater/hotwater-waterheater.html', {'host': settings.DATASERVER_HOST,
                                                                  'heater': heater_name})
