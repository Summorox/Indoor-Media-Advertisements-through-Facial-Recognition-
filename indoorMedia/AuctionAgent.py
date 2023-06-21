import json
import threading
import time
from queue import Queue

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

import network_config
from AdvertisingAgent import AdvertisingAgent


class AuctionAgent(Agent):
    def __init__(self, jid, password, ad_agents):
        super().__init__(jid, password)
        self.ad_agents = ad_agents

    class ReceiveBehaviour(CyclicBehaviour):
        async def run(self):
            msg = network_config.CORE_AUCTION_MESSAGE
            #msg = await self.receive(timeout=10)
            if msg:
                print("[AuctionAgent] Received a message")
                network_config.CORE_AUCTION_MESSAGE = None
                demographic_data = json.loads(msg.body)
                for i, ad_agent in enumerate(self.agent.ad_agents):
                    message = Message(to=ad_agent + network_config.SERVER, body=msg.body)
                    print(f"[AuctionAgent] Sending message to {message.to}")
                    network_config.AD_MESSAGES[i].append(message)
                    #await self.send(message)

                """max_bid = 0
                winning_ad = None
                for i, _ in enumerate(self.agent.ad_agents):
                    if network_config.AD_BIDS_MESSAGES[i]:  # if list not empty
                        msg = network_config.AD_BIDS_MESSAGES[i].pop(0)  # pop the first messagepop the first message
                        #msg = await self.receive(timeout=60)  # wait for all responses
                        if msg:
                            ad, bid = json.loads(msg.body)
                            print("Reached Here")
                            if bid > max_bid:
                                max_bid = bid
                                winning_ad = ad
                        #network_config.AD_MESSAGES[i] = None

                print('WINNING AD')
                print(max_bid)
                print(winning_ad)"""

    class ReceiveAdsBehaviour(CyclicBehaviour):
        async def run(self):
            max_bid = 0
            winning_ad = None
            for i, _ in enumerate(self.agent.ad_agents):
                if network_config.AD_BIDS_MESSAGES[i]:  # if list not empty
                    print("[AuctionAgent] Received a message")
                    msg = network_config.AD_BIDS_MESSAGES[i].pop(0)  # pop the first messagepop the first message
                    # msg = await self.receive(timeout=60)  # wait for all responses
                    if msg:
                        ad, bid = json.loads(msg.body)
                        if bid > max_bid:
                            max_bid = bid
                            winning_ad = ad
            #print('WINNING AD')
            #print(max_bid)
            #print(winning_ad)
            if(winning_ad is not None):
                msgAd = Message(to='core' + network_config.SERVER)
                msgAd.body = json.dumps(winning_ad)
                msgAd.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
                print(f"[AuctionAgent] Sending message to {msgAd.to}")
                network_config.AUCTION_CORE_MESSAGE = msgAd
                winning_ad = None
                #await self.send(msgSend)

    async def setup(self):
        print("AuctionAgent started")
        receiveBehaviour = self.ReceiveBehaviour()
        receiveAdsBehaviour = self.ReceiveAdsBehaviour()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(receiveBehaviour, template)
        self.add_behaviour(receiveAdsBehaviour, template)


    """def auction(self, demographic_data):
        threads = []
        for agent in self.advertisingAgents:
            thread = threading.Thread(target=agent.propose_ad, args=(demographic_data, self.ads_queue))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        return self.choose_ad()

    def choose_ad(self):
        max_bid = 0
        winning_ad = None
        while not self.ads_queue.empty():
            ad, bid = self.ads_queue.get()
            if bid > max_bid:
                max_bid = bid
                winning_ad = ad
        print('WINNING AD')
        print(max_bid)
        print(winning_ad)
        return winning_ad """