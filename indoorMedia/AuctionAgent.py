import json
import threading
import time
from queue import Queue

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

import network_config
from AuctionParticipantAgent import AuctionParticipantAgent


class AuctionAgent(Agent):
    def __init__(self, jid, password, ad_agents):
        super().__init__(jid, password)
        self.ad_agents = ad_agents

    class ReceiveBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive()
            if msg and ("core_agent" in str(msg.sender)):
                print("[AuctionAgent] Received a message")
                demographic_data = json.loads(msg.body)
                for i, ad_agent in enumerate(self.agent.ad_agents):
                    message = Message(to="im_"+ad_agent+"_agent" + network_config.SERVER, body=msg.body)
                    print(f"[AuctionAgent] Sending message to {message.to}")
                    
                    await self.send(message)

    class ReceiveAdsBehaviour(CyclicBehaviour):
        async def run(self):
            max_bid = 0
            winning_ad = None
            for i, agt in enumerate(self.agent.ad_agents):
                #if network_config.AD_BIDS_MESSAGES[i]:  # if list not empty
                    

                msg = await self.receive()  # wait for all responses
                if msg and (agt in str(msg.sender)):
                    print("[AuctionAgent] Received a message")
                    ad, bid = json.loads(msg.body)
                    if bid > max_bid:
                        max_bid = bid
                        winning_ad = ad
            #print('WINNING AD')
            #print(max_bid)
            #print(winning_ad)
            if(winning_ad is not None):
                msgAd = Message(to='im_core_agent' + network_config.SERVER)
                msgAd.body = json.dumps(winning_ad)
                msgAd.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
                print(f"[AuctionAgent] Sending message to {msgAd.to}")
                winning_ad = None
                await self.send(msgAd)

    async def setup(self):
        print("AuctionAgent started")
        receiveBehaviour = self.ReceiveBehaviour()
        receiveAdsBehaviour = self.ReceiveAdsBehaviour()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(receiveBehaviour, template)
        self.add_behaviour(receiveAdsBehaviour, template)


