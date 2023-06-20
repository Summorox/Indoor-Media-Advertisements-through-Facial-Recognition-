import cv2
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template


class DisplayAgent(Agent):

    def __init__(self, jid, password):
        super().__init__(jid, password)

    class ReceiveBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive()
            if msg:
                ad_path = msg.body
                self.agent.display_ad(ad_path)

    async def setup(self):
        print("DisplayAgent started")
        receiveBehaviour = self.ReceiveBehaviour()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(receiveBehaviour, template)

    def display_ad(self, ad_path):
        if ad_path.split('.')[-1] in ['jpeg', 'jpg', 'png']:
            self.display_image(ad_path)
        elif ad_path.split('.')[-1] in ['avi', 'mp4']:
            self.display_video(ad_path)
    def display_image(self, img_path):
        img = cv2.imread(img_path)
        cv2.imshow('Advertisement', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def display_video(self, video_path):
        cap = cv2.VideoCapture(video_path)

        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret:
                cv2.imshow('Advertisement', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()