import paho.mqtt.client as mqtt
import json

# CallBack Function
def on_connect(client, userdata, flags, rc):
    print("Connected with Code : ", str(rc))
    print("userdata: ", userdata)
    # client.subscribe("TestTopic/#")
    # client.subscribe("TestTopic/msg")
    # client.subscribe("hdmi")
    # client.subscribe("TestTopic/JsonData")
    # client.subscribe("TestTopic/JsonDataRcv")

    client.subscribe("iot/eBoard/general/userDefStrs/response")
    
    # client.subscribe("TestTopic/msg")

def on_message(client, userdata, msg):
    # print("msg.payload: ", str(msg.payload))
    # print("msg", str(msg))
    print()
    print("json.loads(msg.payload): ", json.loads(msg.payload))

myUserdata = dict({ "First":1, 
                    "Second":2, 
                    "Third":"Just For Testing"})

client = mqtt.Client(client_id="Leamon's_Mqttsub")
client.user_data_set(myUserdata)
client.on_connect = on_connect
client.on_message = on_message

print(client._client_id)

# client.username_pw_set("xslrwgbm", "GqwmAzMlFHRq")
# client.connect("m15.cloudmqtt.com", 19517, 60)
# client.username_pw_set("xslrwgbm", "GqwmAzMlFHRq")     # client.username_pw_set must be executed before client.connect()

# client.connect("localhost")         # If mosquitto's server is on localhost

# if Weintek is broker itself
client.username_pw_set("xslrwgbm", "GqwmAzMlFHRq")
client.connect("10.101.100.88", 1883, 60)

client.loop_forever()