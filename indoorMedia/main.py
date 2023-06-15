import asyncio

from CoreAgent import CoreAgent
characteristics = ['gender', 'age']

mqtt_broker = '192.168.137.1'
mqtt_port = 1883
mqtt_topic = 'PICTURE'

#img_path=''
img_path = 'happy-friends-from-different-races-culture-laughing_166273-465.jpg'

#core_agent = CoreAgent(model_paths, characteristics, img_path, mqtt_broker, mqtt_port, mqtt_topic)
#core_agent.run()
async def main():
    core = CoreAgent(img_path,mqtt_broker, mqtt_port, mqtt_topic, "advisage_core@localhost", "AdVisage_Core_Pwd")
    await core.start()
asyncio.run(main())
