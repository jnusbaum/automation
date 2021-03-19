from django.urls import path

from devices import views

urlpatterns = [
    path('', views.dashboard, name='view_devices_dashboard'),
    path('all/', views.all_sensors, name='view_devices_all'),
    path('overlay/', views.overlay, name='view_devices_overlay'),
    path('test/<sensor_name>/', views.test, name='view_devices_test'),
    path('<sensor_name>/', views.sensor, name='view_devices_sensor'),
]
