import json
from datetime import datetime
import pytz
import paho.mqtt.client as mqtt
from django.conf import settings
from django.core.management.base import BaseCommand
from sensors.models import DeviceStatus

import logging

logger = logging.getLogger('devstatuscapture')
logger.setLevel('INFO')

MAX_TEMP_MOVE = 25
MIN_TEMP = 25


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    cmd = userdata['command']
    logger.info(f"Connected with result code {rc}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(settings.BASETOPIC + '/device/status/+')


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    cmd = userdata['command']
    # save data to db
    # zone payload is JSON object containing sensor value
    #         {
    #             'device': 'CIRC',
    #             'timestamp': '2020-01-11T14:33:10.772357',
    #             'status': 'RUNNING'
    #         }
    payload = json.loads(msg.payload)
    logger.debug(f"got mesg, payload = {payload}")
    try:
        fsname = payload['device']
    except KeyError:
        # old format status
        # get device name from topic
        tcomp = msg.topic.split('/')
        fsname = tcomp[-1]
    timestamp = datetime.fromtimestamp(payload['timestamp'], tz=pytz.timezone("UTC"))
    timestamp = timestamp.replace(tzinfo=None)
    status = payload['status']
    s = DeviceStatus(device_id=fsname, timestamp=timestamp, status=status)
    s.save()


class Command(BaseCommand):
    help = 'capture device status data'

    def handle(self, *args, **options):
        client = mqtt.Client(client_id=settings.DEVSTATUSMQTTID, clean_session=False,
                             userdata=dict(command=self))
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(settings.MQTTHOST)

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        client.loop_forever()
