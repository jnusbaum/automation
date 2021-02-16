from django.urls import path

from . import api

urlpatterns = [
    # device
    path('devices', api.devices, name='api_devices'),
    path('devices/<device_name>', api.device, name='api_device'),
    path('devices/<device_name>/onewireinterfaces', api.onewireinterfaces_for_device, name='api_onewireinterfaces_for_device'),
    path('devices/<device_name>/tempsensors', api.tempsensors_for_device, name='api_tempsensors_for_device'),
    path('devices/<device_name>/relays', api.relays_for_device, name='api_relays_for_device'),
    path('devices/<device_name>/data', api.device_data, name='api_device_data'),

    # one wire interfaces
    path('onewireinterfaces', api.onewireinterfaces, name='api_onewireinterfaces'),
    path('onewireinterfaces/<ifc_id>', api.onewireinterface, name='api_onewireinterface'),

    # tempsensor
    path('tempsensors', api.tempsensors, name='api_tempsensors'),
    path('tempsensors/<sensor_name>', api.tempsensor, name='api_tempsensor'),
    path('tempsensors/<sensor_name>/data', api.tempsensor_data, name='api_tempsensor_data'),

    # relay
    path('relays', api.tempsensors, name='api_relays'),
    path('relays/<relay_name>', api.relay, name='api_relay'),
    path('relays/<relay_name>/data', api.relay_data, name='api_relay_data'),
]
