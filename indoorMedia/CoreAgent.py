from io import BytesIO

import cv2
import base64
import numpy as np
from PIL import Image

from DecisionMakingAgent import DecisionMakingAgent
from ImageProcessingAgent import ImageProcessingAgent
import paho.mqtt.client as mqtt

class CoreAgent:
    def __init__(self, model_paths, characteristics, img_path, mqtt_broker, mqtt_port, mqtt_topic):
        self.model_paths = model_paths
        self.characteristics = characteristics
        self.img_path = img_path
        self.imageProcessingAgent = ImageProcessingAgent(model_paths)
        self.decisionMakingAgent = DecisionMakingAgent(self.characteristics)

        self.client = mqtt.Client("Core")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.mqtt_topic = mqtt_topic

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(self.mqtt_topic)

    def on_message(self, client, userdata, msg):
        print(msg.payload)
        # Base64 decode the payload
        img_bytes = base64.b64decode(msg.payload)
        image = Image.open(BytesIO(img_bytes))
        image.save('capturar.jpg')
        # Convert the bytes to a numpy array
        nparr = np.frombuffer(img_bytes, np.uint8)
        print(nparr)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            print("Image is empty")
            return
        self.process_image(img)

    def process_image(self, img):
        demographic_data = self.imageProcessingAgent.process_image(img)
        winning_ad = 'ads/'+self.decisionMakingAgent.auction(demographic_data)
        print(winning_ad)

    def publish_ad(self, ad_path):
        client = mqtt.Client('Display')
        client.connect(self.mqtt_broker, self.mqtt_port, 60)
        client.publish(self.display_topic, ad_path)
        print(ad_path)
        client.disconnect()
    def run(self):
        self.client.connect(self.mqtt_broker, self.mqtt_port, 60)
        self.client.loop_forever()

    #def run(self):
        # Get the demographic data from the Image Processing Agent
    #    img = cv2.imread(self.img_path)
    #    demographic_data = self.imageProcessingAgent.process_image(img)
    #    winning_ad = self.decisionMakingAgent.auction(demographic_data)

        #image_test = 'test_image_ad.jpg'
        #video_test = 'test_video_ad.mp4'
   #     if winning_ad.split('.')[-1] in ['jpeg', 'jpg', 'png']:
   #         self.displayAgent.display_image('ads/'+winning_ad)
   #     elif winning_ad.split('.')[-1] in ['avi', 'mp4']:
   #         self.displayAgent.display_video('ads/'+winning_ad)