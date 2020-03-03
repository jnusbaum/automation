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
    cmd = userdata['command']
    cmd.stdout.write("Connected with result code " + str(rc))
    client.subscribe('sorrelhills/device/config-request/+')
    cmd.stdout.write(f"subscribed to sorrelhills/device/config-request/+")


def handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    cmd = userdata['command']
    cmd.stdout.write(f"request received on {msg.topic}")
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
            ojson['num_sensors'] = len(ojson['sensors'])
            djson['interfaces'].append(ojson)
            djson['num_interfaces'] = len(djson['interfaces'])
        jload = json.dumps(djson, default=handler)
        cmd.stdout.write(f"publishing {jload} to sorrelhills/device/config/{device_name}")
        pres = client.publish(f"sorrelhills/device/config/{device_name}", jload)
        if pres.rc != mqtt.MQTT_ERR_SUCCESS:
            cmd.stdout.write(f"error = {pres.rc}")
    except Device.DoesNotExist:
        # error
        cmd.stdout.write("device does not exist")


class Command(BaseCommand):
    help = 'serve configuration data over mqtt'

    def handle(self, *args, **options):
        client = mqtt.Client(client_id=settings.DEVCFGMQTTID, userdata={'command': self})
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(settings.MQTTHOST)

        client.loop_forever()
