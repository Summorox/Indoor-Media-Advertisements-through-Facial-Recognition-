import asyncio
import json
from io import BytesIO

import cv2
import base64
import numpy as np
import spade
from spade.behaviour import OneShotBehaviour
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from DecisionMakingAgent import DecisionMakingAgent
from ImageProcessingAgent import ImageProcessingAgent
import paho.mqtt.client as mqtt

class CoreAgent(Agent):
    def __init__(self, img_path, mqtt_broker, mqtt_port, mqtt_topic, jid, passwd):
        super().__init__(jid, passwd)
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.mqtt_topic = mqtt_topic
        self.img_path = img_path
        self.tracing = True

    class ReceiveBehaviour(spade.behaviour.CyclicBehaviour):
        async def run(self):
            msg = await self.receive()
            if msg:
                print('test')
                demographic_data = json.loads(msg.body)
                # winning_ad = 'ads/' + self.decisionMakingAgent.auction(demographic_data)
                print(demographic_data)
    class RequestBehaviour(OneShotBehaviour):
        async def run(self):
            img = cv2.imread(self.agent.img_path)
            _, img_encoded = cv2.imencode('.jpg', img)
            img_bytes = img_encoded.tobytes()
            img_str = base64.b64encode(img_bytes).decode()
            msg = Message(to="image@localhost")
            msg.body = img_str
            msg.set_metadata("performative", "inform")
            print(f"[CoreAgent] Sending message to {msg.to}")
            await self.send(msg)
            print(f"[CoreAgent] Message sent to {msg.to}")
    async def setup(self):
        print("CoreAgent started")
        receive_behaviour = self.ReceiveBehaviour()
        request_behaviour = self.RequestBehaviour()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(receive_behaviour,template)
        self.add_behaviour(request_behaviour,template)
        #self.client = mqtt.Client("Core")
        #self.client.on_connect = self.on_connect
        #self.client.on_message = self.on_message
        #self.client.connect(self.mqtt_broker, self.mqtt_port, 60)
        #self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(self.mqtt_topic)

    def on_message(self, client, userdata, msg):
        print(msg.payload)
        # Base64 decode the payload
        img_bytes = base64.b64decode(msg.payload)
        # Convert the bytes to a numpy array
        nparr = np.frombuffer(img_bytes, np.uint8)
        print(nparr)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            print("Image is empty")
            return
        asyncio.run(self.process_image(img))

    def publish_ad(self, ad_path):
        client = mqtt.Client('Display')
        client.connect(self.mqtt_broker, self.mqtt_port, 60)
        client.publish(self.display_topic, ad_path)
        print(ad_path)
        client.disconnect()

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