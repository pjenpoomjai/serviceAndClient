import cv2
import tensorflow as tf
import numpy as np
from tensorflow import keras
import os
import paho.mqtt.client as mqtt
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import json

class_names = ['cat','dog']
dirname = os.path.dirname(__file__)

model = keras.Sequential([
keras.layers.Flatten(input_shape=(28,28,3)),
keras.layers.Dense(128, activation=tf.nn.relu),    
keras.layers.Dense(16, activation=tf.nn.relu),    
keras.layers.Dropout(0.2),
keras.layers.Dense(2, activation=tf.nn.softmax)
])

model.compile(optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy'])
model.load_weights('./model/cp-0080.ckpt')

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("imageAB")
def on_message(client, userdata, msg):
    print(time.time())
    a = time.time()
    print ("Topic : ", msg.topic)
    # print(data["byteArr"])
    image = msg.payload
    f = open("./images/tet.jpg", "wb")  #there is a output.jpg which is different
    f.write(image)
    f.close()
    print('Received data.')
    processImage()
    print(time.time() - a )
def run():
    broker_address = "broker.mqttdashboard.com"
    #broker_address = "iot.eclipse.org"
    client.on_connect = on_connect
    client.on_message = on_message  # attach function to callback
    print("connecting to broker")
    client.connect(broker_address)  # connect to broke
    client.loop_forever()

def processImage():
        print("processing")
        image = cv2.imread("./images/tet.jpg", 1)  #there is a output.jpg which is different
        image = cv2.resize(image,(28,28))
        print("resize done.")
        imageArray = np.array(image)
        newFrame = np.array([imageArray]) /255.0
        print("array done.")
        predictions = model.predict(newFrame)
        outputAnimal = class_names[np.argmax(predictions)]
        print("predic done.")
        client.publish("ToClient", outputAnimal)

if __name__ == "__main__":
    client = mqtt.Client('cloudSide')
    run()
