import paho.mqtt.client as mqtt
import time
import json
import random

subTopic = ''

# CallBack Function
def on_connect(client, userdata, flags, rc):
    print("Connected with Code : ", str(rc))
    client.subscribe("/DW/Event")
    client.subscribe("/DW/Event/OP_IN/Result/ACK")
    client.subscribe("/DW/Event/OP_OUT/Result/ACK")
    client.subscribe("/DW/Event/Material_In/Result/ACK")

    
    

def on_message(client, userdata, msg):
    start_Idx = 2
    subTopic = str(msg.payload, encoding="utf-8")[start_Idx:]

    # sTemp = msg.payload[2:].decode("utf-8")
    # sTemp2 = str(msg.payload[2:], encoding="utf-8")
    # print("type: ", type(sTemp))
    # print("type2: ", type(sTemp2))
    
    # Method1
    # sTemp = sTemp.replace("\x00",'')
    # Method2
    # sTemp = sTemp.rstrip("\x00")
    # print("Payload: ", sTemp, " length: ", len(sTemp))

    # remove duplicated spaces
    subTopic = " ".join(subTopic.split())
    # remove all the spaces
    subTopic = subTopic.replace(" ", "")
    if "OP_IN" in subTopic:
        print(1)
        end_Idx = len("OP_IN")
    elif "OP_OUT" in subTopic:
        print(2)
        end_Idx = len("OP_OUT")
    elif "Material_In" in subTopic:
        print(3)
        end_Idx = len("Material_In")
    else:
        print(subTopic)
    subTopic = subTopic[0:end_Idx]
    
    if subTopic.strip() == "OP_IN":   
        print("OP_IN Handler...") 
        client.publish("/DW/Event/OP_IN/Result", "OK,A128664291,Peter Koa", qos=0)
    elif subTopic.strip() == "OP_OUT":
        print("OP_OUT Handler...") 
        client.publish("/DW/Event/OP_OUT/Result", "OK", qos=0)
    elif subTopic.strip() == "Material_In":
        print("Material_In Handler...")
        client.publish("/DW/Event/Material_In/Result", "OK,1,10CA2600**,Copper 8mm", qos=0)


client = mqtt.Client(client_id="Leamon's_Mqttpub")
client.on_connect = on_connect
client.on_message = on_message

client.connect("10.101.100.97", 1883, 60)

client.loop_start()
time.sleep(1)

while True:
    
    time.sleep(1)
    # client.publish("/topic/2", "Hi11,Hi2,Hi3,H6,Hi7,Hi12345699", qos=0)
    

client.loop_stop()
client.disconnect()
