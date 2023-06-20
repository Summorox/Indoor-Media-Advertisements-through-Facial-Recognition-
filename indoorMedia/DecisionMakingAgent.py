import json
import threading
from queue import Queue

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

import network_config
from AdvertisingAgent import AdvertisingAgent


class DecisionMakingAgent(Agent):
    def __init__(self, jid, password, ad_agents):
        super().__init__(jid, password)
        self.ad_agents = ad_agents

    class ReceiveBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                demographic_data = json.loads(msg.body)
                for ad_agent in self.agent.ad_agents:
                    await self.send(Message(to=ad_agent+network_config.SERVER, body=msg.body))

                max_bid = 0
                winning_ad = None

                for _ in self.agent.ad_agents:
                    msg = await self.receive(timeout=60)  # wait for all responses
                    if msg:
                        ad, bid = json.loads(msg.body)
                        if bid > max_bid:
                            max_bid = bid
                            winning_ad = ad

                print('WINNING AD')
                print(max_bid)
                print(winning_ad)
    async def setup(self):
        print("DecisionMakingAgent started")
        receiveBehaviour = self.ReceiveBehaviour()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(receiveBehaviour, template)

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