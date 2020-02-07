import json
from datetime import datetime
import paho.mqtt.client as mqtt
from django.conf import settings
from django.core.management.base import BaseCommand
from heating.models import TempSensorData


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe('sorrelhills/device/config-request/+')


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # publish config data
    msg_pieces = msg.topic.split('/')
    device_name = msg_pieces[-1]

    payload = json.loads(msg.payload)
    fsname = payload['sensor']
    timestamp = datetime.fromisoformat(payload['timestamp'])
    value = payload['value']
    s = TempSensorData(sensor_id=fsname, timestamp=timestamp, value=value, original_value=value)
    s.save()


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
