from django.urls import path
from . import views

urlpatterns = [
    # device
    path('devices/', views.devices, name='api_devices'),
    path('devices/<device_name>/', views.device, name='api_device'),
    path('devices/<device_name>/config/', views.device_config, name='api_device'),
]
