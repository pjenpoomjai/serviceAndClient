import paho.mqtt.client as mqtt  # import the client1
import time
import argparse
import cv2

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ToClient")

def on_message(client, userdata, msg):
    print(time.time())
    a = time.time()
    print ("Topic : ", msg.topic)
    # print(data["byteArr"])
    animal = msg.payload
    print(animal)
    print('Received data.')
    print(time.time() - a )
    client.disconnect()

    
# broker.mqttdashboard.com
parser = argparse.ArgumentParser(description='Sent Image to cloud')
parser.add_argument('--pictureFile', default='somewhere', help='File name')
args = parser.parse_args()
broker_address = "broker.mqttdashboard.com"
#broker_address = "iot.eclipse.org"
print("creating new instance")
client = mqtt.Client('clientSide')  # create new instance
client.on_connect = on_connect
client.on_message = on_message
print("connecting to broker")
client.connect(broker_address)  # connect to broker
#print("Publishing message to topic", "if/test")
# client.publish(topic="nonine", payload= "FALL" ,qos=0)

fileImage = open(args.pictureFile,'rb')
fileImage = fileImage.read()
byteArr = bytearray(fileImage)
print("Publishing message to topic", "image")
client.publish(topic="imageAB", payload= byteArr ,qos=0)


client.loop_forever()
