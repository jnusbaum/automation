from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='view_sensors_dashboard'),
    path('all/', views.all_sensors, name='view_sensors_all'),
    path('overlay/', views.overlay, name='view_sensors_overlay'),
    path('test/<sensor_name>/', views.test, name='view_sensors_test'),
    path('<sensor_name>/', views.sensor, name='view_sensors_sensor'),
]
