import json
import logging

import paho.mqtt.client as mqtt
from django.conf import settings
from django.core.management.base import BaseCommand

from devices.models import Device

logger = logging.getLogger('deviceconfig')


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    cmd = userdata['command']
    logger.info("Connected with result code " + str(rc))
    client.subscribe(f"{settings.BASETOPIC}/device/config-request/+")
    logger.info(f"subscribed to {settings.BASETOPIC}/device/config-request/+")


def on_disconnect(client, userdata, rc):
    cmd = userdata['command']
    if rc != 0:
        logger.error("unexpected disconnect")
    logger.info("disconnected")


def handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    cmd = userdata['command']
    logger.info(f"request received on {msg.topic}")
    # publish config data
    msg_pieces = msg.topic.split('/')
    device_name = msg_pieces[-1]
    try:
        d = Device.objects.get(pk=device_name)
        # one wire temp busses
        djson = {'client_id': d.client_id, 'interfaces': []}
        for onew in d.onewireinterface_set.all():
            ojson = {'pin_number': onew.pin_number, 'devices': []}
            for s in onew.tempsensor_set.all():
                ojson['devices'].append({'name': s.name, 'address': s.address})
            ojson['num_sensors'] = len(ojson['devices'])
            djson['interfaces'].append(ojson)
            djson['num_interfaces'] = len(djson['interfaces'])
        # digital relays
        for rnew in d.relay_set.all():
            djson['relay'] = {'name': rnew.name, 'pin_number': rnew.pin_number}
        jload = json.dumps(djson, default=handler)
        logger.info(f"publishing {jload} to {settings.BASETOPIC}/device/config/{device_name}")
        pres = client.publish(f"{settings.BASETOPIC}/device/config/{device_name}", jload)
        if pres.rc != mqtt.MQTT_ERR_SUCCESS:
            logger.error(f"error = {pres.rc}")
    except Device.DoesNotExist:
        # error
        logger.warning("device does not exist")


class Command(BaseCommand):
    help = 'serve configuration data over mqtt'

    def handle(self, *args, **options):
        client = mqtt.Client(client_id=settings.DEVCFGMQTTID, userdata={'command': self})
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect
        client.connect(settings.MQTTHOST)

        client.loop_forever()
