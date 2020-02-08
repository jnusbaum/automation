import json
from datetime import datetime
import paho.mqtt.client as mqtt
from django.conf import settings
from django.core.management.base import BaseCommand
from heating.models import Device


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    print("Connected with result code " + str(rc))
    client.subscribe('sorrelhills/device/config-request/+')


def handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # publish config data
    msg_pieces = msg.topic.split('/')
    device_name = msg_pieces[-1]
    try:
        d = Device.objects.get(pk=device_name)
        djson = {'client_id': d.client_id}
        djson['interfaces'] = []
        for onew in d.onewireinterface_set.all():
            ojson = {'pin_number': onew.pin_number}
            ojson['sensors'] = []
            for s in onew.tempsensor_set.all():
                ojson['sensors'].append({'name': s.name, 'address': s.address})
            djson['interfaces'].append(ojson)
        jload = json.dumps(djson, default=handler)
        pres = client.publish(f"sorrelhills/device/config/{device_name}", jload)
        if pres.rc != mqtt.MQTT_ERR_SUCCESS:
            print(f"error = {pres.rc}")
    except Device.DoesNotExist:
        # error
        print("device does not exist")


class Command(BaseCommand):
    help = 'capture sensor data'

    def handle(self, *args, **options):
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(settings.MQTTHOST)

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        client.loop_forever()
