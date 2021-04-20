from django.conf import settings
from django.shortcuts import render

from heating.models import Zone, Boiler, MixingValve
from hotwater.models import CircPump, WaterHeater


def dashboard(request):
    return render(request, 'automation/automation-dashboard.html', {'host': settings.DATASERVER_HOST})


def plot(request):
    dzones = []
    dboilers = []
    dvalves = []
    dpumps = []
    dheaters = []
    zones = Zone.objects.all().order_by('name')
    boilers = Boiler.objects.all().order_by('name')
    valves = MixingValve.objects.all().order_by('name')
    pumps = CircPump.objects.all().order_by('name')
    heaters = WaterHeater.objects.all().order_by('name')
    if 'ALL' in request.GET:
        for z in zones:
            dzones.append(z.name)
        for b in boilers:
            dboilers.append(b.name)
        for v in valves:
            dvalves.append(v.name)
        for c in pumps:
            dpumps.append(c.name)
        for h in heaters:
            dheaters.append(h.name)
    else:
        for z in zones:
            if z.name in request.GET:
                dzones.append(z.name)
        for b in boilers:
            if b.name in request.GET:
                dboilers.append(b.name)
        for v in valves:
            if v.name in request.GET:
                dvalves.append(v.name)
        for p in pumps:
            if p.name in request.GET:
                dpumps.append(p.name)
        for h in heaters:
            if h.name in request.GET:
                dheaters.append(h.name)
    return render(request, 'automation/automation-plot.html', {'host': settings.DATASERVER_HOST,
                                                                'zones': dzones,
                                                                'boilers': dboilers,
                                                                'valves': dvalves,
                                                                'pumps': dpumps,
                                                                'heaters': dheaters,
                                                            })