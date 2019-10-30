import paho.mqtt.client as mqtt
import time
import json
import random

sPayload = ''

# CallBack Function
def on_connect(client, userdata, flags, rc):
    print("Connected with Code : ", str(rc))
    
    client.subscribe("/+/Event")
    client.subscribe("/+/Event/OP_IN/Result/ACK")
    client.subscribe("/+/Event/OP_OUT/Result/ACK")
    client.subscribe("/+/Event/Material_In/Result/ACK")
    client.subscribe("/+/Event/Material_Out/Result/ACK")


def on_message(client, userdata, msg):
    start_Idx = 2
    print("Raw data: ", msg.payload)
    sPayload = str(msg.payload, encoding="utf-8")[start_Idx:]
    sPayload = sPayload.rstrip("\x00")
    print("Topic: ", msg.topic, " length: ", len(msg.topic))
    print("Payload: ", sPayload, " length: ", len(sPayload))
    
    print()


client = mqtt.Client(client_id="Leamon's_MqttSimu")
client.on_connect = on_connect
client.on_message = on_message

client.connect("10.101.100.97", 1883, 60)

client.loop_forever()
