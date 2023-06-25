import base64
import json

import cv2
import numpy as np
import paho.mqtt.client as mqtt
from spade.behaviour import OneShotBehaviour
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import spade
import network_config


class ImageProcessingAgent(Agent):
    def __init__(self, model_paths, jid, passwd):
        super().__init__(jid, passwd)
        self.model_paths = model_paths
        self.tracing = True
    class ReceiveBehaviour(spade.behaviour.CyclicBehaviour):
        async def run(self):
            #msg = network_config.CORE_IMAGE_MESSAGE
            msg = await self.receive(timeout=5)
            if msg:
                network_config.CORE_IMAGE_MESSAGE = None
                print(msg)
                print("[ImageProcessingAgent] Received a message")
                img_bytes = base64.b64decode(msg.body)
                nparr = np.frombuffer(img_bytes, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                if img is None:
                    print("Image is empty")
                    return
                demographic_data = await self.agent.process_image(img)
                if demographic_data:
                    print(demographic_data)
                    msg = Message(to='im_core_agent' + network_config.SERVER)
                    msg.body = json.dumps(demographic_data)
                    msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
                    
                    print(f"[ImageProcessingAgent] Sending message to {msg.to}")
                    await self.send(msg)
                else:
                    print("[ImageProcessingAgent] No faces detected in the image, not sending message")
    async def setup(self):
        print("ImageProcessingAgent started 1")
        self.frame_width, self.frame_height = 1280, 720
        self.age_net = cv2.dnn.readNetFromCaffe(self.model_paths['age_proto'], self.model_paths['age_model'])
        self.face_net = cv2.dnn.readNetFromCaffe(self.model_paths['face_proto'], self.model_paths['face_model'])
        self.gender_net = cv2.dnn.readNetFromCaffe(self.model_paths['gender_proto'], self.model_paths['gender_model'])

        self.MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
        self.AGE_INTERVALS = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)',
                              '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
        self.GENDER_LIST = ['Male', 'Female']

        print("ImageProcessingAgent started 2")
        receiveBehaviour = self.ReceiveBehaviour()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(receiveBehaviour,template)

    def get_faces(self, frame, confidence_threshold=0.5):
        # convert the frame into a blob to be ready for NN input
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104, 177.0, 123.0))
        # set the image as input to the NN
        self.face_net.setInput(blob)
        # perform inference and get predictions
        output = np.squeeze(self.face_net.forward())
        # initialize the result list
        faces = []
        # Loop over the faces detected
        for i in range(output.shape[0]):
            confidence = output[i, 2]
            if confidence > confidence_threshold:
                box = output[i, 3:7] * \
                      np.array([frame.shape[1], frame.shape[0],
                                frame.shape[1], frame.shape[0]])
                # convert to integers
                start_x, start_y, end_x, end_y = box.astype(int)
                # widen the box a little
                start_x, start_y, end_x, end_y = start_x - \
                                                 10, start_y - 10, end_x + 10, end_y + 10
                start_x = 0 if start_x < 0 else start_x
                start_y = 0 if start_y < 0 else start_y
                end_x = 0 if end_x < 0 else end_x
                end_y = 0 if end_y < 0 else end_y
                # append to our list
                faces.append((start_x, start_y, end_x, end_y))
        return faces

    def get_gender_predictions(self, face_img):
        blob = cv2.dnn.blobFromImage(
            image=face_img, scalefactor=1.0, size=(227, 227),
            mean=self.MODEL_MEAN_VALUES, swapRB=False, crop=False
        )
        self.gender_net.setInput(blob)
        return self.gender_net.forward()

    def get_age_predictions(self, face_img):
        blob = cv2.dnn.blobFromImage(
            image=face_img, scalefactor=1.0, size=(227, 227),
            mean=self.MODEL_MEAN_VALUES, swapRB=False
        )
        self.age_net.setInput(blob)
        return self.age_net.forward()

    async def process_image(self, input_img):
        frame = cv2.resize(input_img, (self.frame_width, self.frame_height))
        faces = self.get_faces(frame)

        results = []
        for i, face_coords in enumerate(faces):
            start_x, start_y, end_x, end_y = face_coords
            face_img = frame[start_y:end_y, start_x:end_x].copy()

            age_predictions = self.get_age_predictions(face_img)
            gender_predictions = self.get_gender_predictions(face_img)

            age = self.AGE_INTERVALS[age_predictions[0].argmax()]
            gender = self.GENDER_LIST[gender_predictions[0].argmax()]

            results.append({
                "gender": gender,
                "age": age
            })
            # do something with the age and gender results (e.g., print them out)
        return results
