from django.urls import path

from . import api

urlpatterns = [
    # zone
    path('zones', api.zones, name='api_zones'),
    path('zones/<zone_name>', api.zone, name='api_zone'),
    path('zones/<zone_name>/sensors', api.sensors_for_zone, name='api_sensors_for_zone'),
    path('zones/<zone_name>/data', api.zone_data, name='api_zone_data'),
]
