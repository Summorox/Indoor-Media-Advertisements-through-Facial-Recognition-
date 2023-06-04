class DecisionMakingAgent:
    def __init__(self, queue):
        self.queue = queue

    def choose_ad(self):
        max_bid = 0
        winning_ad = None
        while not self.queue.empty():
            ad, bid = self.queue.get()
            print(ad)
            print(bid)
            if bid > max_bid:
                max_bid = bid
                winning_ad = ad
        return winning_ad