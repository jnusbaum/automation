import json
from datetime import datetime
import paho.mqtt.client as mqtt
from django.conf import settings
from django.core.management.base import BaseCommand
from heating.models import TempSensorData

MIN_TEMP = 25

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(settings.TOPIC)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # save data to db
    # zone payload is JSON object containing sensor value
    #         {
    #             'sensor': 'BOILER-IN',
    #             'timestamp': '2020-01-11T14:33:10.772357',
    #             'value': 142.3
    #         }
    payload = json.loads(msg.payload)
    fsname = payload['sensor']
    timestamp = datetime.fromisoformat(payload['timestamp'])
    value = payload['value']
    ovalue = value
    print(f"saving {fsname}, {timestamp}, {value}")
    # need to do some kind of basic data cleaning here
    if value < MIN_TEMP:
        value = MIN_TEMP
    
    userdata[fsname] = value
    # save previous value, if new value "significantly" different from previous, then wait for next value to confirm?
    s = TempSensorData(sensor_id=fsname, timestamp=timestamp, value=value, original_value=ovalue)
    s.save()


class Command(BaseCommand):
    help = 'capture sensor data'

    def handle(self, *args, **options):
        value_cache = {}
        client = mqtt.Client(userdata=value_cache)
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(settings.MQTTHOST)

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        client.loop_forever()
