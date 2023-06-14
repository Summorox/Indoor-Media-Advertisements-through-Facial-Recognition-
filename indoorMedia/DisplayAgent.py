import cv2
from paho import mqtt


class DisplayAgent:

    def __init__(self, mqtt_broker, mqtt_port, mqtt_topic):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.mqtt_topic = mqtt_topic

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(self.mqtt_topic)

    def on_message(self, client, userdata, msg):
        ad_path = msg.payload.decode()  # Decode the message payload
        self.display_ad(ad_path)

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

    def display_ad(self, ad_path):
        if ad_path.split('.')[-1] in ['jpeg', 'jpg', 'png']:
            self.display_image(ad_path)
        elif ad_path.split('.')[-1] in ['avi', 'mp4']:
            self.display_video(ad_path)

    def run(self):
        self.client.connect(self.mqtt_broker, self.mqtt_port, 60)
        self.client.loop_forever()