from indoorMedia.DisplayAgent import DisplayAgent

mqtt_broker = 'mqtt_broker'
mqtt_port = 1883
mqtt_topic = 'DISPLAY'

display_agent = DisplayAgent(mqtt_broker, mqtt_port, mqtt_topic)
display_agent.run()