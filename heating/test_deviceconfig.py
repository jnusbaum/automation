import pprint

import json
import paho.mqtt.client as mqtt

def handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("sorrelhills/device/config/+")
    client.publish("sorrelhills/device/config-request/MECHROOM")


def on_message(client, userdata, msg):
    # publish config data
    msg_pieces = msg.topic.split('/')
    device_name = msg_pieces[-1]
    payload = json.loads(msg.payload)
    print(device_name)
    pprint.pprint(payload)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.134", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()