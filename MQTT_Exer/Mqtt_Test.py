import paho.mqtt.publish as publisher
import time


strHost = "m15.cloudmqtt.com"
strAuth = {"username": "xslrwgbm", "password": "GqwmAzMlFHRq"}

strTopic = "TestTopic/"
strPayLoad = "This is the message from single() method"

client_id = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
# client = mqtt.Client(client_id)                   # ClientId can't duplicate so we use time to differentiate it

publisher.single(strTopic, strPayLoad, client_id=client_id, qos=1, hostname=strHost, auth=strAuth, port=19517)

print("Message sent ... ")


