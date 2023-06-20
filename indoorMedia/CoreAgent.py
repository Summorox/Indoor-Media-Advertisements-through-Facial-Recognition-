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
import network_config

class CoreAgent(Agent):
    def __init__(self, img_path, mqtt_broker, mqtt_port, mqtt_topic, jid, passwd):
        super().__init__(jid, passwd)
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.mqtt_topic = mqtt_topic
        self.img_path = img_path
        self.tracing = True
        self.imageReceived = None

    class ReceiveBehaviour(CyclicBehaviour):
        async def run(self):
            #msg = network_mock.DEMOGRAPHICS_MESSAGE
            msg = await self.receive()
            if msg:
                if("image"+network_config.SERVER ==str(msg.sender)):
                    #network_mock.DEMOGRAPHICS_MESSAGE= None
                    print('test')
                    demographic_data = json.loads(msg.body)
                    # winning_ad = 'ads/' + self.decisionMakingAgent.auction(demographic_data)
                    print(demographic_data)
                    msgAuction = Message(to="auctiont"+network_config.SERVER)
                    msgAuction.body = json.dumps(demographic_data)
                    msgAuction.set_metadata("performative", "inform")
                    await self.send(msgAuction)
                elif("auction"+network_config.SERVER == str(msg.sender)):
                    winning_ad = msg.body
                    msgDisplay = Message(to="display"+network_config.SERVER)
                    print(winning_ad)
                    msgDisplay.body =winning_ad
                    msgDisplay.set_metadata("performative", "inform")
                    await self.send(msgDisplay)
    class RequestBehaviour(CyclicBehaviour):
        async def run(self):
            if(self.agent.imageReceived is not None):
                img = cv2.imread(self.agent.imageReceived)
                self.agent.imageReceived = None
                _, img_encoded = cv2.imencode('.jpg', img)
                img_bytes = img_encoded.tobytes()
                img_str = base64.b64encode(img_bytes).decode()
                msg = Message(to="image@localhost")
                msg.body = img_str
                msg.set_metadata("performative", "inform")
                print(f"[CoreAgent] Sending message to {msg.to}")
                #network_mock.IMAGE_MESSAGE = msg
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
        else:
            self.image_received = img
