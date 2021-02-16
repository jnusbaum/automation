import json
from datetime import datetime
import pytz
import paho.mqtt.client as mqtt
from django.conf import settings
from django.core.management.base import BaseCommand
from devices.models import RelayData

import logging

logger = logging.getLogger('relaycapture')
logger.setLevel('INFO')

MAX_TEMP_MOVE = 25
MIN_TEMP = 25


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    cmd = userdata['command']
    logger.info(f"Connected with result code {rc}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(settings.BASETOPIC + '/relay/+')


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    cmd = userdata['command']
    # save data to db
    # zone payload is JSON object containing sensor value
    #         {
    #             'relay': 'CIRC',
    #             'timestamp': '2020-01-11T14:33:10.772357',
    #             'value': true
    #         }
    payload = json.loads(msg.payload)
    logger.debug(f"got mesg, payload = {payload}")
    fsname = payload['relay']
    timestamp = datetime.fromtimestamp(payload['timestamp'], tz=pytz.timezone("UTC"))
    timestamp = timestamp.replace(tzinfo=None)
    value = payload['value']
    s = RelayData(relay_id=fsname, timestamp=timestamp, value=value)
    s.save()


class Command(BaseCommand):
    help = 'capture relay data'

    def handle(self, *args, **options):
        client = mqtt.Client(client_id=settings.RELAYMQTTID, clean_session=False,
                             userdata=dict(command=self))
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(settings.MQTTHOST)

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        client.loop_forever()
