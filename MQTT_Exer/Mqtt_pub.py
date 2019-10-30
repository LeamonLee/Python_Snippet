import paho.mqtt.client as mqtt
import time
import json
import random

# CallBack Function
def on_connect(client, userdata, flags, rc):
    print("Connected with Code : ", str(rc))
    client.subscribe("TestTopic/#")
    client.subscribe("hdmi/content/json")

def on_message(client, userdata, msg):
    print("msg: ", msg)
    print(str(msg.payload))
    print(msg.topic)
    print(msg.qos)


client = mqtt.Client(client_id="Leamon's_Mqttpub")
client.on_connect = on_connect
client.on_message = on_message

# client.username_pw_set("xslrwgbm", "GqwmAzMlFHRq")
# client.connect("m15.cloudmqtt.com", 19517, 60)
# client.username_pw_set("xslrwgbm", "GqwmAzMlFHRq")     # client.username_pw_set must be executed before client.connect()

# client.connect("localhost")             # If mosquitto's server is on localhost

# if Weintek is broker itself
client.username_pw_set("xslrwgbm", "GqwmAzMlFHRq")
client.connect("10.101.100.88", 1883, 60)

#client.loop_forever()
client.loop_start()
time.sleep(1)

JsonData = dict()
JsonData['d'] = {
    "value 1": [True],
    "value 2": ["HiPa"]
}
JsonDumpData = json.dumps(JsonData)
print("JsonData: ", JsonData)
print("json.dumps(JsonData): ", JsonDumpData)


eBoardJsonData = dict()
# eBoardJsonData['d'] = {
#     "string1": "Hello1",
#     "string2": "Hello2",
#     "string3": "Hello3",
#     "string4": "Hello4",
#     "string5": "Hello5",
#     "string6": "Hello6",
#     "string7": "Hello7",
#     "string8": "Hello8",
#     "string9": "Hello9",
#     "string10": "Hello10\nMan",
#     "confirmToken": 99999,
#     "confirmFlag": True
# }

eBoardJsonData['d'] = {
    "string1": "Energy management",
    "string2": "OEE function",
    "string3": "Live data scope",
    "string4": "Head up display",
    "string5": "Recipe function",
    "string6": "Marketing",
    "string7": "Hello7",
    "string8": "Hello8",
    "string9": "Hello9",
    "string10": "Happy Valentine's Day!",
    "confirmToken": 99999,
    "confirmFlag": True,
    "string_enable1": True,
    "string_enable2": True,
    "string_enable3": True,
    "string_enable4": True,
    "string_enable5": True,
    "string_enable6": True,
    "string_enable7": False,
    "string_enable8": False,
    "string_enable9": False,
    "string_enable10": True
}

eBoardJsonDumpData = json.dumps(eBoardJsonData)
print("eBoardJsonData: ", eBoardJsonData)
print("json.dumps(eBoardJsonData): ", eBoardJsonDumpData)

while True:
    # client.publish("TestTopic/", "Getting started with MQTT")
    # my_str = "Hello pal_"
    my_str = "Hello pal1"
    print(my_str)
    
    my_str_as_bytes = str.encode(my_str)
    print(my_str_as_bytes)
    
    my_decoded_str = my_str_as_bytes.decode()
    print(my_decoded_str)
    
    client.publish("TestTopic/msg", "Hello pal_")
    client.publish("TestTopic/JsonDataRcv", JsonDumpData)


    myRandomNum = random.getrandbits(32)
    myRandomNum = abs(myRandomNum)
    print(myRandomNum)
    eBoardJsonData["d"]["confirmToken"] = myRandomNum
    eBoardJsonDumpData = json.dumps(eBoardJsonData)
    client.publish("iot/eBoard/general/userDefStrs", eBoardJsonDumpData)

    # client.publish("hdmi/content/json", "Hello pal", qos=1)
    # client.publish("hdmi", 100, qos=2)
    print("Publisher sent message to CloudMQTT")
    time.sleep(5)

client.loop_stop()
client.disconnect()
