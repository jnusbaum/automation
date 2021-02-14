from . import settings
from django.shortcuts import render

from sensors.models import Device


def dashboard(request):
    device = Device.objects.get(id=settings.HWCIRCDEVICE)
    return render(request, 'hwcirc/hwcirc-dashboard.html',
                          {'host': settings.DATASERVER_HOST, 'zone': zone_name, 'zones': zones})

