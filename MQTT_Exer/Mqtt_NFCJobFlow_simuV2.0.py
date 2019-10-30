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
    
    if  msg.topic == "/DW/Event" or msg.topic == "/STR/Event":
        if "OP_IN" in sPayload:
            print("OP_IN Event Handler...") 
            # client.publish("/DW/Event/OP_IN/Result", "OK,A128664291,Peter Koa", qos=1)
            client.publish(msg.topic + "/OP_IN/Result", "OK,A128664291,Peter Koa", qos=1)
            
        elif "OP_OUT" in sPayload:
            print("OP_OUT Event Handler...") 
            # client.publish("/DW/Event/OP_OUT/Result", "OK", qos=1)
            client.publish(msg.topic + "/OP_OUT/Result", "OK", qos=1)

        elif "Material_In" in sPayload:
            print("Material_In Event Handler...")
            # client.publish("/DW/Event/Material_In/Result", "OK,1,10CA2600**,Copper 8mm", qos=1)
            
            lstPayload = sPayload.split(",")
            if int(lstPayload[1]) == 1:
                client.publish(msg.topic + "/Material_In/Result", "OK,1,10CA2600**,Copper 8mm", qos=1)
            elif int(lstPayload[1]) == 2:
                client.publish(msg.topic + "/Material_In/Result", "OK,2,10CA2600**,Copper 8mm", qos=1)
            elif int(lstPayload[1]) == 3:
                client.publish(msg.topic + "/Material_In/Result", "OK,3,10CA2600**,Copper 8mm", qos=1)
            else:
                client.publish(msg.topic + "/Material_In/Result", "NG", qos=1)
            
            time.sleep(1)

        elif "Material_Out" in sPayload:
            print("Material_Out Event Handler...")
            # client.publish("/DW/Event/Material_Out/Result", "OK,1,JBS3863621", qos=1)
            lstPayload = sPayload.split(",")
            if int(lstPayload[1]) == 1:
                client.publish(msg.topic + "/Material_Out/Result", "OK,1,JBS3863621", qos=1)
            elif int(lstPayload[1]) == 2:
                client.publish(msg.topic + "/Material_Out/Result", "OK,2,JBS7432211", qos=1)
            elif int(lstPayload[1]) == 3:
                client.publish(msg.topic + "/Material_Out/Result", "OK,3,JBS9947273", qos=1)
            else:
                client.publish(msg.topic + "/Material_Out/Result", "NG", qos=1)
            
            time.sleep(1)

    elif (msg.topic.startswith("/DW/Event/") and msg.topic.endswith("/Result/ACK")) or \
         (msg.topic.startswith("/STR/Event/") and msg.topic.endswith("/Result/ACK")):

        if msg.topic.startswith("/DW/Event/"):
            sSubTopic = msg.topic[len("/DW/Event/"):-len("/Result/ACK")]
        else:
            sSubTopic = msg.topic[len("/STR/Event/"):-len("/Result/ACK")]
        
        print("sSubTopic: ", sSubTopic)
        if sSubTopic == "Material_In":
            lstResult = sPayload.split(',')
            print("Number: ", lstResult[1])
            print("TimeStamp: ", lstResult[2])
            print("Product Name: ", lstResult[3])
            print("Length: ", lstResult[4])
            print("JobID: ", lstResult[5])
        elif sSubTopic == "Material_Out":
            lstResult = sPayload.split(',')
            print("Number: ", lstResult[1])
            print("TimeStamp: ", lstResult[2])
            print("Product Name: ", lstResult[3])
            print("Length: ", lstResult[4])
            print("JobID: ", lstResult[5])
        else:
            if sPayload == "ACK":
                print("ACK Received...")
            else:
                print(sPayload)
        print()


client = mqtt.Client(client_id="Leamon's_MqttSimu")
client.on_connect = on_connect
client.on_message = on_message

client.connect("10.101.100.97", 1883, 60)

client.loop_forever()
