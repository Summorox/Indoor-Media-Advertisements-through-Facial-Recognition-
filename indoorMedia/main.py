from CoreAgent import CoreAgent
model_paths = {
    'face_proto': 'deployproto.prototxt',
    'face_model': 'res10_300x300_ssd_iter_140000_fp16.caffemodel',
    'age_proto': 'deploy_age.prototxt',
    'age_model': 'age_net.caffemodel',
    'gender_proto': 'deploy_gender.prototxt',
    'gender_model': 'gender_net.caffemodel',
}
characteristics = ['gender', 'age']

mqtt_broker = 'broker.hivemq.com'
mqtt_port = 1883
mqtt_topic = 'PICTURE_FCR'

mqtt_display_broker = 'mqtt_broker'
mqtt_display_topic = 'DISPLAY'

#camera_agent = CameraAgent(mqtt_broker, mqtt_port, mqtt_topic)
#camera_agent.capture_and_send_image()
#camera_agent.close()

img_path = ''
#img_path = 'happy-friends-from-different-races-culture-laughing_166273-465.jpg'

core_agent = CoreAgent(model_paths, characteristics, img_path, mqtt_broker, mqtt_port, mqtt_topic,mqtt_display_broker,mqtt_display_topic)
core_agent.run()
