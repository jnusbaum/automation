from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='view_heating_dashboard'),
    path('weather/<weather_name>/', views.weather, name='view_heating_weather'),
    path('zone/<zone_name>/', views.zone, name='view_heating_zone'),
    path('boiler/<boiler_name>/', views.boiler, name='view_heating_boiler'),
    path('mixingvalve/<valve_name>/', views.mixingvalve, name='view_heating_mixingvalve'),
]
