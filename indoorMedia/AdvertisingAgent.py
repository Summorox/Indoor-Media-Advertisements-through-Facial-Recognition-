import asyncio
import json
import time

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

import network_config


class AdvertisingAgent(Agent):
    def __init__(self, jid, password, characteristic):
        super().__init__(jid, password)
        self.characteristic = characteristic
        with open('ads_database.json', 'r') as f:
            self.ads_database = json.load(f)
    class ReceiveBehaviour(CyclicBehaviour):
        async def run(self):
            for i, characteristic in enumerate(['gender', 'age', 'age_gender']):
                max_bid = 0
                max_ad_info = None
                if self.agent.characteristic == characteristic and network_config.AD_MESSAGES[i]:  # if list not empty
                    msg = network_config.AD_MESSAGES[i].pop(0)  # pop the first message
                    # msg = await self.receive()
                    print("[AdvertisingAgent]" + self.agent.characteristic + " Received a message")
                    demographic_data = json.loads(msg.body)
                    for data in demographic_data:
                        age_range = list(map(int, data['age'].strip('()').split(', ')))
                        if self.agent.characteristic == 'gender':
                            filtered_ads = [ad for ad in self.agent.ads_database if
                                            ad['gender'] == data['gender'] and ad['age'] == 'Empty']
                            network_config.AD_MESSAGES[0] = None
                        elif self.agent.characteristic == 'age':
                            filtered_ads = [ad for ad in self.agent.ads_database if
                                            ad['age'] == age_range and ad['gender'] == 'Empty']
                            network_config.AD_MESSAGES[1] = None
                        elif self.agent.characteristic == "age_gender":
                            filtered_ads = [ad for ad in self.agent.ads_database if
                                            ad['gender'] == data['gender'] and ad['age'] == age_range]
                            network_config.AD_MESSAGES[2] = None
                        if filtered_ads:
                            ad_info = max(filtered_ads, key=lambda x: x['money_to_display'])
                            num_people = len(
                                [d for d in demographic_data if
                                 d['gender'] == data['gender'] and d['age'] == data['age']])
                            bid = ad_info['money_to_display'] * num_people
                            if bid > max_bid:
                                max_bid = bid
                                max_ad_info = ad_info
                if max_ad_info is not None:
                    response_msg = Message(to='auction' + network_config.SERVER)
                    response_msg.body = json.dumps((max_ad_info['ad_file'], max_bid))
                    network_config.AD_BIDS_MESSAGES[i].append(response_msg)
                    #await self.send(response_msg)

    async def setup(self):
        print(f"AdvertisingAgent {self.jid.localpart} started")
        receiveBehaviour = self.ReceiveBehaviour()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(receiveBehaviour)

    """def propose_ad(self, demographic_data, queue):
        for data in demographic_data:
            # Extract age range from string format and convert to list of integers
            age_range = list(map(int, data['age'].strip('()').split(', ')))
            if self.characteristic == 'gender':
                filtered_ads = [ad for ad in self.ads_database if
                                ad['gender'] == data['gender'] and ad['age'] == 'Empty']
            elif self.characteristic == 'age':
                filtered_ads = [ad for ad in self.ads_database if ad['age'] == age_range and ad['gender'] == 'Empty']
            else:  # characteristic is 'both'
                filtered_ads = [ad for ad in self.ads_database if
                                ad['gender'] == data['gender'] and ad['age'] == age_range]

            print('Agent: ' + self.characteristic + ' - ' + str(age_range) + ' - ' + data['gender'])
            if filtered_ads:
                ad_info = max(filtered_ads, key=lambda x: x['money_to_display'])
                num_people = len(
                    [d for d in demographic_data if d['gender'] == data['gender'] and d['age'] == data['age']])
                bid = ad_info['money_to_display'] * num_people
                queue.put((ad_info['ad_file'], bid))"""
