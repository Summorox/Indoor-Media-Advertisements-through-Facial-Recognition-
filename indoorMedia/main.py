from CameraAgent import CameraAgent
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

mqtt_broker = 'mqtt_broker'
mqtt_port = 1883
mqtt_topic = 'image_processing/input'

camera_agent = CameraAgent(mqtt_broker, mqtt_port, mqtt_topic)
camera_agent.capture_and_send_image()
camera_agent.close()

img_path = 'capture.jpg'

core_agent = CoreAgent(model_paths, characteristics, img_path)
core_agent.run()
