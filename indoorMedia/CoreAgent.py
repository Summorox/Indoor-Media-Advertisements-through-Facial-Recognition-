import cv2
from DecisionMakingAgent import DecisionMakingAgent
from DisplayAgent import DisplayAgent
from ImageProcessingAgent import ImageProcessingAgent

class CoreAgent:
    def __init__(self, model_paths, characteristics, img_path):
        self.model_paths = model_paths
        self.characteristics = characteristics
        self.img_path = img_path
        self.imageProcessingAgent = ImageProcessingAgent(model_paths)
        self.displayAgent = DisplayAgent()
        self.decisionMakingAgent = DecisionMakingAgent(self.characteristics)

    def run(self):
        # Get the demographic data from the Image Processing Agent
        img = cv2.imread(self.img_path)
        demographic_data = self.imageProcessingAgent.process_image(img)
        winning_ad = self.decisionMakingAgent.auction(demographic_data)

        #image_test = 'test_image_ad.jpg'
        #video_test = 'test_video_ad.mp4'
        if winning_ad.split('.')[-1] in ['jpeg', 'jpg', 'png']:
            self.displayAgent.display_image('ads/'+winning_ad)
        elif winning_ad.split('.')[-1] in ['avi', 'mp4']:
            self.displayAgent.display_video('ads/'+winning_ad)