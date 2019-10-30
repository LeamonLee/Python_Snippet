# coding: utf-8
import paho.mqtt.client as mqtt
import time
import os
import signal
import sys
import imp
import threading

# print("Current encoding: ", sys.getdefaultencoding())
# imp.reload(sys)
# sys.setdefaultencoding('utf-8')
# print("Changed module..." )
# print("Current encoding: ", sys.getdefaultencoding())


class mqttThread(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self, daemon=True)
        self.mqtt_looping = True
        self.num = num
        self.strHost = "m15.cloudmqtt.com"
        self.strAuth = {"username": "xslrwgbm", "password": "GqwmAzMlFHRq"}
        self.nPort = 19517
        # self.nPort = 19516

        self.strTopic = "TestTopic/"
        self.strPayLoad = "This is the message from single() method"

        self.client = None

    '''
    rc Connection Return Codes:
    0: Connection successful
    1: Connection refused – incorrect protocol version
    2: Connection refused – invalid client identifier
    3: Connection refused – server unavailable
    4: Connection refused – bad username or password
    5: Connection refused – not authorised
    6-255: Currently unused.
    '''
    # CallBack Function

    def on_connect(self, mq, userdata, flags, rc):
        if rc == 0:
            print("Connected OK with returned code=", str(rc))
        else:
            print("Bad connection with returned code={0} - {1}".format(str(rc), mqtt.connack_string(rc)))

    def on_disconnect(self, mq, userdata, rc):
        if rc != 0:
            print("Unexpected disconnection. Returned code={0}".format(rc))
        else:
            print("The connection is off.")

    def on_message(self, mq, userdata, msg):
        print("topic: %s" % msg.topic)
        print("payload: %s" % msg.payload)
        print("qos: %d" % msg.qos)

    def on_publish(self, mq, userdata, mid):
        print("mid: ", mid)

    def on_log(self, mq, userdata, level, string):
        print("Logging from Mqtt: ", string)

    def mqtt_client_thread(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.client.on_log = self.on_log
        while self.mqtt_looping:
            try:
                self.client.username_pw_set(
                    self.strAuth["username"], self.strAuth["password"])
                self.client.connect(self.strHost, self.nPort, keepalive=60)
                print("Connect succeed...")
                break
            except:
                print("Connected to MQTT Broker failed... ")
        
        # self.client.loop_forever()
        self.client.loop_start()
        time.sleep(1)

        while self.mqtt_looping:
            self.client.publish("Tutorial/", "Getting started with MQTT")
            self.client.publish("TestTopic/", "Hello pal")
            print("Publisher sent message to CloudMQTT")
            time.sleep(5)

        self.client.loop_stop() 
        print("Mqtt thread quit...")
        self.client.disconnect()


    def stop(self, *args):
        self.mqtt_looping = False
        #self.client.disconnect()
        print("Quit mqtt thread...")


    def run(self):
        while self.mqtt_looping:
            print("My Thread {0} Class is Running".format(self.num))
            self.mqtt_client_thread()
            time.sleep(1)


if __name__ == '__main__':
    
    mqtt_th = mqttThread(99)

    signal.signal(signal.SIGTERM, mqtt_th.stop)
    signal.signal(signal.SIGQUIT, mqtt_th.stop)
    signal.signal(signal.SIGINT,  mqtt_th.stop)  # Ctrl-C

    mqtt_th.start()

    mqtt_th.join()

    print("exit program")
    sys.exit(0)
