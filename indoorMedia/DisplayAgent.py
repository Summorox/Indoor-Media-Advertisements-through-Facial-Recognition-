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
            msg = network_config.CORE_DISPLAY_MESSAGE
            #msg = await self.receive()
            if msg:
                print(f"[DisplayAgent] Received Message")
                network_config.CORE_DISPLAY_MESSAGE = None
                ad_path = msg.body
                stripped_path = "\"zara_dress15.png\""
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

    """def display_ad(self, ad_path):
        if ad_path.split('.')[-1] in ['jpeg', 'jpg', 'png']:
            self.display_image(ad_path)
        elif ad_path.split('.')[-1] in ['avi', 'mp4']:
            self.display_video(ad_path)
    def display_image(self, img_path):
        img = cv2.imread(img_path)
        if img is None:
            print(f"Could not open or find the image: {img_path}")
            return
        print('test')
        cv2.imshow('Advertisement', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def display_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        if cap is None:
            print(f"Could not open or find the video: {video_path}")
            return
        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret:
                cv2.imshow('Advertisement', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()"""