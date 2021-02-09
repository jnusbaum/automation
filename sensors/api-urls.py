from django.urls import path

from . import api

urlpatterns = [
    # device
    path('devices', api.devices, name='api_devices'),
    path('devices/<device_name>', api.device, name='api_device'),
    path('devices/<device_name>/sensors', api.sensors_for_device, name='api_sensors_for_device'),
    path('devices/<device_name>/data', api.device_data, name='api_device_data'),
    path('devices/<device_name>/config', api.device_config, name='api_device_config'),
    # sensor
    path('sensors', api.sensors, name='api_sensors'),
    path('sensors/<sensor_name>', api.sensor, name='api_sensor'),
    path('sensors/<sensor_name>/data', api.sensor_data, name='api_sensor_data'),
]
