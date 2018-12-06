import paho.mqtt.client as mqtt
import os

def on_connect(client, userdata, flags, rc):
    client.subscribe("detect")


def on_message(client, userdata, msg):
    if msg.topic == "detect":
		if msg.payload == "Detect":
			os.system("python detector.py")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

try:
	client.loop_forever()
except KeyboardInterrupt:
	client.loop_stop()
	print "Client Disconnect"
	print "Close Database"
