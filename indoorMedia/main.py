import asyncio
import time

import network_config
from AdvertisingAgent import AdvertisingAgent
from CoreAgent import CoreAgent
from DecisionMakingAgent import DecisionMakingAgent
from DisplayAgent import DisplayAgent
from ImageProcessingAgent import ImageProcessingAgent

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

ad_agents = ["gender", "age", "age_gender"]


imageAgent = ImageProcessingAgent(model_paths, "image"+network_config.SERVER, "password")

coreAgent = CoreAgent(img_path,mqtt_broker, mqtt_port, mqtt_topic, "core"+network_config.SERVER, "password")

auctionAgent = DecisionMakingAgent("auction"+network_config.SERVER, "password", ad_agents)

displayAgent = DisplayAgent("display"+network_config.SERVER, "password")

advertising_agents = []
for i, characteristic in enumerate(ad_agents):
    agent = AdvertisingAgent(f"{characteristic}"+network_config.SERVER, "password", characteristic)
    advertising_agents.append(agent)

async def stopAgents():
    future_image = imageAgent.stop()
    await future_image  # Wait for future_image to complete before starting the coreAgent
    future_core = coreAgent.stop()
    await future_core
    future_auction = auctionAgent.stop()
    await future_auction
    for agent in advertising_agents:
        await agent.stop()
    future_display = displayAgent.stop()
    await future_display

async def runAgents():
    future_image = imageAgent.start()
    await future_image  # Wait for future_image to complete before starting the coreAgent
    time.sleep(2)
    future_auction = auctionAgent.start()
    await future_auction
    for agent in advertising_agents:
        time.sleep(2)
        future_advertising = agent.start()
        await future_advertising
    time.sleep(2)
    future_display = displayAgent.start()
    await  future_display
    time.sleep(2)
    future_core = coreAgent.start()
    await future_core

asyncio.run(runAgents())
