import asyncio
import time

import network_config
from AuctionParticipantAgent import AuctionParticipantAgent
from CoreAgent import CoreAgent
from AuctionAgent import AuctionAgent
from DisplayAgent import DisplayAgent
from ImageProcessingAgent import ImageProcessingAgent

mqtt_broker = '192.168.137.1'
mqtt_port = 1883
mqtt_topic = 'PICTURE'

#img_path=''
img_path = '1Female_Child.jpg'
model_paths = {
            'face_proto': 'deployproto.prototxt',
            'face_model': 'res10_300x300_ssd_iter_140000_fp16.caffemodel',
            'age_proto': 'deploy_age.prototxt',
            'age_model': 'age_net.caffemodel',
            'gender_proto': 'deploy_gender.prototxt',
            'gender_model': 'gender_net.caffemodel',
        }

ad_agents = ["gender", "age", "age_gender"]


imageAgent = ImageProcessingAgent(model_paths, "image"+network_config.SERVER, "image")

coreAgent = CoreAgent(img_path,mqtt_broker, mqtt_port, mqtt_topic, "core"+network_config.SERVER, "core")

auctionAgent = AuctionAgent("auction" + network_config.SERVER, "auction", ad_agents)

displayAgent = DisplayAgent("display"+network_config.SERVER, "display")

advertising_agents = []
for i, characteristic in enumerate(ad_agents):
    agent = AuctionParticipantAgent(f"{characteristic}" + network_config.SERVER, "password", characteristic)
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
    future_auction = auctionAgent.start()
    await future_auction
    future_display = displayAgent.start()
    await  future_display
    for agent in advertising_agents:
        future_advertising = agent.start()
        await future_advertising
    future_core = coreAgent.start()
    future_core2 = coreAgent.web.start(hostname="127.0.0.1",port="10000")
    await future_core
    await future_core2

asyncio.run(runAgents())

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break
coreAgent.stop()
imageAgent.stop()
auctionAgent.stop()
displayAgent.stop()
for agent in advertising_agents:
    agent.stop()