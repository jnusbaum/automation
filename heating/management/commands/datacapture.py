import json
from datetime import datetime
import paho.mqtt.client as mqtt
from django.conf import settings
from django.core.management.base import BaseCommand
from heating.models import TempSensorData

import logging
logger = logging.getLogger('datacapture')

MAX_TEMP_MOVE = 25
MIN_TEMP = 25

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    cmd = userdata['command']
    logger.info(f"Connected with result code {rc}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(settings.TOPIC)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    cmd = userdata['command']
    cache = userdata['cache']
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
    try:
        prev = cache[fsname]
        if (value < MIN_TEMP) or (abs(value - prev) > MAX_TEMP_MOVE):
            logger.info(f"replacing {value} with {prev} for {fsname}, {timestamp}")
            value = prev
        else:
            cache[fsname] = value
    except KeyError:
        if value < MIN_TEMP:
            logger.info(f"replacing {value} with {MIN_TEMP} for {fsname}, {timestamp}")
            value = MIN_TEMP
        else:
            cache[fsname] = value

    s = TempSensorData(sensor_id=fsname, timestamp=timestamp, value=value, original_value=ovalue)
    s.save()


class Command(BaseCommand):
    help = 'capture sensor data'

    def handle(self, *args, **options):
        value_cache = {}
        client = mqtt.Client(client_id=settings.DCMQTTID, clean_session=False, userdata={'cache': value_cache, 'command': self})
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(settings.MQTTHOST)

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        client.loop_forever()
