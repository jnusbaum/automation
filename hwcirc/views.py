from django.conf import settings
from django.shortcuts import render


def dashboard(request):
    return render(request, 'hwcirc/hwcirc-dashboard.html')

