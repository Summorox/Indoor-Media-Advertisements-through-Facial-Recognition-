import json

class AdvertisingAgent:
    def __init__(self, characteristic):
        self.characteristic = characteristic
        with open('ads_database.json', 'r') as f:
            self.ads_database = json.load(f)

    def propose_ad(self, demographic_data, queue):
        for data in demographic_data:
            # Extract age range from string format and convert to list of integers
            age_range = list(map(int, data['age'].strip('()').split(', ')))
            filtered_ads = [ad for ad in self.ads_database if ad['gender'] == data['gender'] and ad['age'] == age_range]
            print('Agent: ' + self.characteristic+ ' - ' + str(age_range) + ' - ' +data['gender'])
            if filtered_ads:
                ad_info = max(filtered_ads, key=lambda x: x['money_to_display'])
                num_people = len(
                    [d for d in demographic_data if d['gender'] == data['gender'] and d['age'] == data['age']])
                bid = ad_info['money_to_display'] * num_people
                queue.put((ad_info['ad_file'], bid))
