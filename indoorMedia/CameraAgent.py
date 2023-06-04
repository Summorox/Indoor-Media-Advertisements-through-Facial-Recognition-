import cv2
import paho.mqtt.client as mqtt
import numpy as np

class CameraAgent:
    def __init__(self, mqtt_broker, mqtt_port, mqtt_topic, camera_id=0):
        self.camera = cv2.VideoCapture(camera_id)
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.mqtt_topic = mqtt_topic
        #self.client = mqtt.Client()

    def capture_and_send_image(self):
        # Capture frame-by-frame
        ret, frame = self.camera.read()

        # Ensure the capture was successful
        if not ret:
            print("Failed to capture image")
            return

        cv2.imwrite('capture.jpg', frame)

        # Convert the image to a byte array
        _, buffer = cv2.imencode('.jpg', frame)
        img_bytes = buffer.tobytes()

        # Publish the image to the MQTT topic
        #self.client.connect(self.mqtt_broker, self.mqtt_port, 60)
        #self.client.publish(self.mqtt_topic, img_bytes)

    def close(self):
        # When everything is done, release the capture
        self.camera.release()
        cv2.destroyAllWindows()