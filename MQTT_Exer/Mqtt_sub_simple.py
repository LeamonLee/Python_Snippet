import paho.mqtt.client as mqtt
import json

nCount = 0

# CallBack Function
def on_connect(client, userdata, flags, rc):
    print("Connected with Code : ", str(rc))
    print("userdata: ", userdata)
    # client.subscribe("topic/#")
    # client.subscribe("topic1/#")
    # client.subscribe("/topic1")
    client.subscribe("/topic/1", qos=0)
    # client.subscribe("/topic/2", qos=0)
    # client.subscribe("/OEE/10.101.100.86/code/2001", qos=0)
    # client.subscribe("/OEE/10.101.100.86/code/2003", qos=0)
    # client.subscribe("/OEE/10.101.100.86/code/3000", qos=0)
    # client.subscribe("/plc/info", qos=1)

    

def on_message(client, userdata, msg):
    
    # print("type: ", type(msg.payload))
    print(msg.payload)
    global nCount
    nCount += 1
    # print("nCount: ", nCount)
    # If the data type is bytes, have to convert into string first.
    # print(msg.payload.decode("utf-8"))
    # print(str(msg.payload, encoding="utf-8"))
    # print(str(msg.payload, encoding="utf-8")[2:])
    # print("json.loads(msg.payload): ", json.loads(msg.payload))


myUserdata = dict({ "First":1, 
                    "Second":2, 
                    "Third":"Just For Testing"})

client = mqtt.Client(client_id="Leamon's_Mqttsub")
client.user_data_set(myUserdata)
client.on_connect = on_connect
client.on_message = on_message

print("client._client_id: ", client._client_id)


client.connect("10.101.100.95", 1883, 60)

client.loop_forever()