import json

import cv2
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
import requests

import network_config


class DisplayAgent(Agent):

    def __init__(self, jid, password):
        super().__init__(jid, password)

    class ReceiveBehaviour(CyclicBehaviour):
        async def run(self):

            msg = await self.receive()
            if msg:
                print(f"[DisplayAgent] Received Message")
                ad_path = msg.body
                stripped_path = "\""+ad_path+"\""
                stripped_path = stripped_path.strip("\"")
                self.agent.display_ad(network_config.ADS_PATH+stripped_path)

    async def setup(self):
        print("DisplayAgent started")
        receiveBehaviour = self.ReceiveBehaviour()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(receiveBehaviour, template)

    def display_ad(self, ad_path):
        print(ad_path)
        display_service_url = 'http://localhost:50000/display'  # Replace with the actual URL of the display service
        headers = {'Content-Type': 'application/json'}  # set Content-Type to application/json
        data = json.dumps({'ad_path': ad_path})  # convert the data to a JSON string
        response = requests.post(display_service_url, data=data, headers=headers)
        if response.status_code != 200:
            print(f"Failed to send ad to display service: {response.text}")

