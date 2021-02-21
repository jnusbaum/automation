from django.conf import settings
from django.shortcuts import render


def dashboard(request):
    return render(request, 'automation/automation-dashboard.html', {'host': settings.DATASERVER_HOST})


