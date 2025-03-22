from django.urls import path

from . import views

urlpatterns = [
    # device
    path('devices/', views.devices, name='api_devices'),
    path('devices/<device_name>/', views.device, name='api_device'),
    path('devices/<device_name>/config/', views.device_config, name='api_device'),
    path('devices/<device_name>/tempsensors/', views.tempsensors_for_device, name='api_tempsensors_for_device'),
    path('devices/<device_name>/relays/', views.relays_for_device, name='api_relays_for_device'),
    path('devices/<device_name>/data/', views.device_data, name='api_device_data'),

    # one wire interfaces
    path('onewireinterfaces/', views.onewireinterfaces, name='api_onewireinterfaces'),
    path('onewireinterfaces/<ifc_id>/', views.onewireinterface, name='api_onewireinterface'),

    # sunsensor
    path('sunsensors/', views.sunsensors, name='api_sunsensors'),
    path('sunsensors/<sensor_name>/', views.sunsensor, name='api_sunsensor'),
    path('sunsensors/<sensor_name>/data/', views.sunsensor_data, name='api_sunsensor_data'),

    # tempsensor
    path('tempsensors/', views.tempsensors, name='api_tempsensors'),
    path('tempsensors/<sensor_name>/', views.tempsensor, name='api_tempsensor'),
    path('tempsensors/<sensor_name>/data/', views.tempsensor_data, name='api_tempsensor_data'),

    # windsensor
    path('windsensors/', views.windsensors, name='api_windsensors'),
    path('windsensors/<sensor_name>/', views.windsensor, name='api_windsensor'),
    path('windsensors/<sensor_name>/data/', views.windsensor_data, name='api_windsensor_data'),

    # relay
    path('relays/', views.relays, name='api_relays'),
    path('relays/<relay_name>/', views.relay, name='api_relay'),
    path('relays/<relay_name>/data/', views.relay_data, name='api_relay_data'),
]
