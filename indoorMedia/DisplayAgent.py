from paho import mqtt


class DisplayAgent:
    def __init__(self, broker, port, topic):
        #self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.topic = topic

    def display_ad(self, ad):
        # Connect to the MQTT broker
        self.client.connect(self.broker, self.port)

        # Publish the ad to the specified MQTT topic
        self.client.publish(self.topic, ad)

        # Disconnect from the MQTT broker
        self.client.disconnect()