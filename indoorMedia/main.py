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


imageAgent = ImageProcessingAgent(model_paths, "im_image_agent"+network_config.SERVER, "Spade123")

coreAgent = CoreAgent(img_path,mqtt_broker, mqtt_port, mqtt_topic, "im_core_agent"+network_config.SERVER, "Spade123")

auctionAgent = AuctionAgent("im_auction_agent" + network_config.SERVER, "Spade123", ad_agents)

displayAgent = DisplayAgent("im_display_agent"+network_config.SERVER, "Spade123")

advertising_agents = []
for i, characteristic in enumerate(ad_agents):
    agent = AuctionParticipantAgent("im_" + f"{characteristic}"+"_agent" + network_config.SERVER, "Spade123", characteristic)
    advertising_agents.append(agent)

async def stopAgents():
    future_image = imageAgent.stop()
    future_image.result()  # Wait for future_image to complete before starting the coreAgent
    future_core = coreAgent.stop()
    future_core.result()
    future_auction = auctionAgent.stop()
    future_auction.result()
    for agent in advertising_agents:
        agent.stop()
    future_display = displayAgent.stop()
    future_display.result()

async def runAgents():
    future_image = imageAgent.start()
    future_image.result()  # Wait for future_image to complete before starting the coreAgent
    future_auction = auctionAgent.start()
    future_auction.result()
    future_display = displayAgent.start()
    future_display.result()
    for agent in advertising_agents:
        future_advertising = agent.start()
        future_advertising.result()

    coreAgent.start().result()
    future_core = coreAgent.web.start(hostname="127.0.0.1",port="10000")
    future_core.result()


asyncio.run(runAgents())

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break
coreAgent.stop().result()
imageAgent.stop().result()
auctionAgent.stop().result()
displayAgent.stop().result()
for agent in advertising_agents:
    agent.stop().result()