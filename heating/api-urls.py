from django.urls import path

from . import api

urlpatterns = [
    path('heating/zones/', api.zones, name='api_zones'),
    path('heating/zones/<zone_name>/', api.zone, name='api_zone'),
    path('heating/zones/<zone_name>/data/', api.zone_data, name='api_zone_data'),
    path('heating/sensors/', api.sensors, name='api_sensors'),
    path('heating/sensors/<sensor_name>/', api.sensor, name='api_sensor'),
    path('heating/sensors/<sensor_name>/data/', api.sensor_data, name='api_sensor_data'),
    path('heating/sensors/zone/<zone_name>/', api.sensors_for_zone, name='api_sensors_for_zone'),
]
