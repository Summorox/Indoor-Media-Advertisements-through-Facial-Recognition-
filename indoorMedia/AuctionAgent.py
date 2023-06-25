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
        self.current_winner = ''
        self.current_winning_ad=''
        self.current_winning_bid = 0
        self.bids_counter = 0

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
            
            msg = await self.receive()  # wait for a message for 5 seconds
            if msg and ("core_agent" not in str(msg.sender)):
                ad, bid = json.loads(msg.body)
                print("[AuctionAgent] Received a message from" + str(msg.sender))
                self.agent.bids_counter = self.agent.bids_counter + 1
                if bid > self.agent.current_winning_bid:
                    self.agent.current_winner = msg.sender
                    self.agent.current_winning_ad = ad
                    self.agent.current_winning_bid = bid
                if self.agent.bids_counter >= len(self.agent.ad_agents):
                    print('Agent '+str(self.agent.current_winner) +' is the WINNER with a bid of: ' +str(self.agent.current_winning_bid))
                    print('Winning Ad: '+self.agent.current_winning_ad)
                    msgAd = Message(to='im_core_agent' + network_config.SERVER)
                    msgAd.body = json.dumps(self.agent.current_winning_ad)
                    msgAd.set_metadata("performative", "inform")  
                    print(f"[AuctionAgent] Sending message to {msgAd.to}")
                    self.current_winner = ''
                    self.current_winning_ad = ''
                    self.current_winning_bid = 0
                    self.bids_counter = 0
                    await self.send(msgAd)

    async def setup(self):
        print("AuctionAgent started")
        receiveBehaviour = self.ReceiveBehaviour()
        receiveAdsBehaviour = self.ReceiveAdsBehaviour()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(receiveBehaviour, template)
        self.add_behaviour(receiveAdsBehaviour, template)


