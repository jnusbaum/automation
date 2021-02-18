from django.shortcuts import render


def dashboard(request):
    return render(request, 'devices/devices-dashboard.html')


def all_sensors(request):
    pass


def overlay(request):
    pass


def test(request):
    pass


def sensor(request):
    pass
