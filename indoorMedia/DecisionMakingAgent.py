import threading
from queue import Queue

from AdvertisingAgent import AdvertisingAgent


class DecisionMakingAgent:
    def __init__(self, characteristics):
        self.characteristics = characteristics
        self.ads_queue = Queue()
        self.advertisingAgents = [AdvertisingAgent(characteristic) for characteristic in self.characteristics]

    def auction(self, demographic_data):
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
        return winning_ad