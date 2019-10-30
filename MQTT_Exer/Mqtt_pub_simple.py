import paho.mqtt.client as mqtt
import time
import json
import random

# CallBack Function
def on_connect(client, userdata, flags, rc):
    print("Connected with Code : ", str(rc))
    client.subscribe("topicFromPLC/#")
    client.subscribe("myWill/#")
    

def on_message(client, userdata, msg):
    print("msg: ", msg)
    print("type: ", type(msg.payload))
    print(str(msg.payload))


client = mqtt.Client(client_id="Leamon's_Mqttpub")
client.on_connect = on_connect
client.on_message = on_message

# client.connect("127.0.0.1", 1883, 60)             # If mosquitto's server is on localhost
client.connect("10.101.100.95", 1883, 60)

client.loop_start()
time.sleep(1)

while True:
    # client.publish("/topic/1", "Getting started with MQTT1")
    time.sleep(1)
    client.publish("/topic/1", "Hi there", qos=0)
    time.sleep(1)
    # client.publish("/topic/3", "Getting started with MQTT3")
    # client.publish("/topic/4", "Getting started with MQTT4")
    # client.publish("/topic/5", "1,2,3,4,5,6")
    # print("Publisher sent message to CloudMQTT")
    time.sleep(1)

client.loop_stop()
client.disconnect()
