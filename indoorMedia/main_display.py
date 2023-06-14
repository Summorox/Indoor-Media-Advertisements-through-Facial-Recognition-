from indoorMedia.DisplayAgent import DisplayAgent

mqtt_broker = 'broker.hivemq.com'
mqtt_port = 1883
mqtt_topic = 'DISPLAY_FCR'

display_agent = DisplayAgent(mqtt_broker, mqtt_port, mqtt_topic)
display_agent.run()