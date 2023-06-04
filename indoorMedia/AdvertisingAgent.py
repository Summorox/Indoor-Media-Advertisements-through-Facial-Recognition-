class AdvertisingAgent:
    def __init__(self, characteristic):
        self.characteristic = characteristic

    def propose_ad(self, demographic_data, queue):
        # For each demographic data, propose an advertisement from an external ad API based on the characteristic
        # Also assign a bid for the opportunity to display the ad
        for data in demographic_data:
            ad = f"Ad for {data[self.characteristic]}"  # replace with actual API call
            bid = 10  # replace with actual bidding logic
            queue.put((ad, bid))