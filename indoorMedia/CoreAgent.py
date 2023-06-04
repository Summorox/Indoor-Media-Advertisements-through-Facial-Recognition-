import threading
from queue import Queue
import cv2
from DecisionMakingAgent import DecisionMakingAgent
from ImageProcessingAgent import ImageProcessingAgent
from AdvertisingAgent import AdvertisingAgent

class CoreAgent:
    def __init__(self, model_paths, characteristics, img_path):
        self.model_paths = model_paths
        self.characteristics = characteristics
        self.img_path = img_path
        self.imageProcessingAgent = ImageProcessingAgent(model_paths, 'mqtt_broker', 1883, 'image_processing/output')
        self.ads_queue = Queue()
        self.advertisingAgents = [AdvertisingAgent(characteristic) for characteristic in self.characteristics]
        self.decisionMakingAgent = DecisionMakingAgent(self.ads_queue)

    def run(self):
        # Get the demographic data from the Image Processing Agent
        img = cv2.imread(self.img_path)
        demographic_data = self.imageProcessingAgent.process_image(img)

        # Start a thread for each Advertising Agent
        threads = []
        for agent in self.advertisingAgents:
            thread = threading.Thread(target=agent.propose_ad, args=(demographic_data, self.ads_queue))
            thread.start()
            threads.append(thread)

        # Wait for all agents to finish
        for thread in threads:
            thread.join()

        # Run the Decision-making Agent to select the winning ad
        winning_ad = self.decisionMakingAgent.choose_ad()
        print('WINNING AD')
        print(winning_ad)