from django.urls import path

from . import views

urlpatterns = [
    path('', views.api_index, name='api_index'),
    path('sensors', views.api_sensors, name='api_sensors'),
    path('sensors/<sensor_name>', views.api_sensor, name='api_sensor'),
    path('sensors/<sensor_name>/data', views.api_sensor_data, name='api_sensor_data'),
]