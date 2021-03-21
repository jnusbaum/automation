from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='view_devices_dashboard'),
    path('all/', views.all_sensors, name='view_devices_all'),
    path('test/<sensor_name>/', views.test, name='view_devices_test'),
    path('<sensor_name>/', views.sensor, name='view_devices_sensor'),
]
