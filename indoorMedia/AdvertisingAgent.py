import json

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template


class AdvertisingAgent(Agent):
    def __init__(self, jid, password, characteristic):
        super().__init__(jid, password)
        self.characteristic = characteristic
        with open('ads_database.json', 'r') as f:
            self.ads_database = json.load(f)

        self.ad_proposal_behaviour = None

    class ReceiveBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive()
            if msg:
                demographic_data = json.loads(msg.body)
                for data in demographic_data:
                    age_range = list(map(int, data['age'].strip('()').split(', ')))
                    if self.agent.characteristic == 'gender':
                        filtered_ads = [ad for ad in self.agent.ads_database if
                                        ad['gender'] == data['gender'] and ad['age'] == 'Empty']
                    elif self.agent.characteristic == 'age':
                        filtered_ads = [ad for ad in self.agent.ads_database if
                                        ad['age'] == age_range and ad['gender'] == 'Empty']
                    elif self.agent.characteristic =="age_gender":
                        filtered_ads = [ad for ad in self.agent.ads_database if
                                        ad['gender'] == data['gender'] and ad['age'] == age_range]

                    if filtered_ads:
                        ad_info = max(filtered_ads, key=lambda x: x['money_to_display'])
                        num_people = len(
                            [d for d in demographic_data if d['gender'] == data['gender'] and d['age'] == data['age']])
                        bid = ad_info['money_to_display'] * num_people

                        response_msg = Message(to=msg.sender)
                        response_msg.body = json.dumps((ad_info['ad_file'], bid))
                        await self.send(response_msg)

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
