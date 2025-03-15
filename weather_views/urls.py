from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='view_weather_dashboard'),
    path('sensor/', views.sensor, name='view_weather_sensor'),
]
