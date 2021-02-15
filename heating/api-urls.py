from django.urls import path

from . import api

urlpatterns = [
    # zone
    path('zones', api.zones, name='api_zones'),
    path('zones/<zone_name>', api.zone, name='api_zone'),
    path('zones/<zone_name>/sensors', api.sensors_for_zone, name='api_sensors_for_zone'),
    path('zones/<zone_name>/data', api.zone_data, name='api_zone_data'),

    path('boilers', api.boilers, name='api_boilers'),
    path('boilers/<boiler_name>', api.boiler, name='api_boiler'),
    path('boilers/<boiler_name>/sensors', api.sensors_for_boiler, name='api_sensors_for_boiler'),
    path('boilers/<boiler_name>/data', api.boiler_data, name='api_boiler_data'),

    path('mixingvalves', api.mixingvalves, name='api_mixingvalves'),
    path('mixingvalves/<valve_name>', api.mixingvalve, name='api_mixingvalve'),
    path('mixingvalves/<valve_name>/sensors', api.sensors_for_mixingvalve, name='api_sensors_for_mixingvalve'),
    path('mixingvalves/<valve_name>/data', api.mixingvalve_data, name='api_mixingvalve_data'),

]
