from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('all/', views.all_sensors, name='view_all'),
    path('overlay/', views.overlay, name='view_overlay'),
    path('test/<sensor_name>/', views.test, name='view_test'),
    path('<sensor_name>/', views.sensor, name='view_sensor'),
]
