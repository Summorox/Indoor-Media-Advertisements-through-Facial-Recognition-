import asyncio
import time

from CoreAgent import CoreAgent
from indoorMedia.ImageProcessingAgent import ImageProcessingAgent

characteristics = ['gender', 'age']

mqtt_broker = '192.168.137.1'
mqtt_port = 1883
mqtt_topic = 'PICTURE'

#img_path=''
img_path = 'happy-friends-from-different-races-culture-laughing_166273-465.jpg'
model_paths = {
            'face_proto': 'deployproto.prototxt',
            'face_model': 'res10_300x300_ssd_iter_140000_fp16.caffemodel',
            'age_proto': 'deploy_age.prototxt',
            'age_model': 'age_net.caffemodel',
            'gender_proto': 'deploy_gender.prototxt',
            'gender_model': 'gender_net.caffemodel',
        }
#core_agent = CoreAgent(model_paths, characteristics, img_path, mqtt_broker, mqtt_port, mqtt_topic)
#core_agent.run()

imageAgent = ImageProcessingAgent(model_paths, "image@localhost", "password")

coreAgent = CoreAgent(img_path,mqtt_broker, mqtt_port, mqtt_topic, "core@localhost", "password")

async def stopAgents():
    future_image = imageAgent.stop()
    await future_image  # Wait for future_image to complete before starting the coreAgent
    future_core = coreAgent.stop()
    await future_core

async def runAgents():
    future_image = imageAgent.start()
    await future_image  # Wait for future_image to complete before starting the coreAgent
    time.sleep(2)
    future_core = coreAgent.start()
    await future_core

asyncio.run(runAgents())
