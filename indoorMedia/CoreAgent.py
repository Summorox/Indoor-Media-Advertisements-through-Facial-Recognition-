import json

import cv2
import base64
import numpy as np
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

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

    class ReceiveImageBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive()
            if msg and ('im_image_agent' in str(msg.sender)):
                print(f"[CoreAgent] Received Message")

                demographic_data = json.loads(msg.body)
                msgAuction = Message(to="im_auction_agent"+network_config.SERVER)
                msgAuction.body = json.dumps(demographic_data)
                msgAuction.set_metadata("performative", "inform")
                print(f"[CoreAgent] Sending message to {msgAuction.to}")

                await self.send(msgAuction)
    class ReceiveAdBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive()
            if msg and ('im_auction_agent' in str(msg.sender)):
                print(f"[CoreAgent] Received Message")
                winning_ad = msg.body
                msgDisplay = Message(to="im_display_agent"+network_config.SERVER)
                print(winning_ad)
                msgDisplay.body =winning_ad
                msgDisplay.set_metadata("performative", "inform")
                
                print(f"[CoreAgent] Sending message to {msgDisplay.to}")
                await self.send(msgDisplay)

    class RequestImageBehaviour(CyclicBehaviour):
        async def run(self):
            image = network_config.IMG_MESSAGE
            #image = cv2.imread(self.agent.img_path)
            if(image is not None):
                
                _, img_encoded = cv2.imencode('.jpg', image)
                img_bytes = img_encoded.tobytes()
                img_str = base64.b64encode(img_bytes).decode()
                cv2.imwrite("capturar.png",image)
                msg = Message(to="im_image_agent"+network_config.SERVER)
                msg.body = img_str
                msg.set_metadata("performative", "inform")

                print(f"[CoreAgent] Sending message to {msg.to}")
                await self.send(msg)
                print(f"[CoreAgent] Message sent to {msg.to}")

    async def setup(self):
        print("CoreAgent started")
        receive_image_behaviour = self.ReceiveImageBehaviour()
        request_image_behaviour = self.RequestImageBehaviour()
        receive_ad_behaviour = self.ReceiveAdBehaviour()
        
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(receive_image_behaviour,template)
        self.add_behaviour(request_image_behaviour,template)
        self.add_behaviour(receive_ad_behaviour,template)

        self.client = mqtt.Client("Core")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.mqtt_broker, self.mqtt_port, 60)
        self.client.loop_start()

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
            print("Received image")
            network_config.IMG_MESSAGE = img
