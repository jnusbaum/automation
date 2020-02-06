from django.urls import path

from . import api

urlpatterns = [
    # zone
    path('heating/zones', api.zones, name='api_zones'),
    path('heating/zones/<zone_name>', api.zone, name='api_zone'),
    path('heating/zones/<zone_name>/sensors', api.sensors_for_zone, name='api_sensors_for_zone'),
    path('heating/zones/<zone_name>/data', api.zone_data, name='api_zone_data'),
    # device
    path('heating/devices', api.devices, name='api_devices'),
    path('heating/devices/<device_name>', api.device, name='api_device'),
    path('heating/devices/<device_name>/sensors', api.sensors_for_device, name='api_sensors_for_device'),
    path('heating/devices/<device_name>/data', api.device_data, name='api_device_data'),
    path('heating/devices/<device_name>/config', api.device_config, name='api_device_config'),
    # sensor
    path('heating/sensors', api.sensors, name='api_sensors'),
    path('heating/sensors/<sensor_name>', api.sensor, name='api_sensor'),
    path('heating/sensors/<sensor_name>/data', api.sensor_data, name='api_sensor_data'),
    path('heating/sensors/zone/<zone_name>', api.sensors_for_zone, name='api_sensors_for_zone'),
]
