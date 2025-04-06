from django.urls import path

from . import views

urlpatterns = [
    # zone
    path('zones/', views.zones, name='api_zones'),
    path('zones/<zone_name>/', views.zone, name='api_zone'),
    path('zones/<zone_name>/devices_views/', views.sensors_for_zone, name='api_sensors_for_zone'),
    path('zones/<zone_name>/data/', views.zone_data, name='api_zone_data'),

    path('boilers/', views.boilers, name='api_boilers'),
    path('boilers/<boiler_name>/', views.boiler, name='api_boiler'),
    path('boilers/<boiler_name>/data/', views.boiler_data, name='api_boiler_data'),

    path('mixingvalves/', views.mixingvalves, name='api_mixingvalves'),
    path('mixingvalves/<valve_name>/', views.mixingvalve, name='api_mixingvalve'),
    path('mixingvalves/<valve_name>/data/', views.mixingvalve_data, name='api_mixingvalve_data'),

    path('weathers/', views.weathers, name='api_weathers'),
    path('weathers/<weather_name>/', views.weather, name='api_weather'),
    path('weathers/<weather_name>/data/', views.weather_data, name='api_weather_data'),
]
