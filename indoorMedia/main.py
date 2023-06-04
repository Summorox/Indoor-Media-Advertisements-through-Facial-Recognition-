import cv2

from ImageProcessingAgent import ImageProcessingAgent

model_paths = {
    'face_proto': 'deployproto.prototxt',
    'face_model': 'res10_300x300_ssd_iter_140000_fp16.caffemodel',
    'age_proto': 'deploy_age.prototxt',
    'age_model': 'age_net.caffemodel',
    'gender_proto': 'deploy_gender.prototxt',
    'gender_model': 'gender_net.caffemodel',
}

agent = ImageProcessingAgent(model_paths, 'mqtt_broker', 1883, 'image_processing/output')

img = cv2.imread('happy-friends-from-different-races-culture-laughing_166273-465.jpg')
agent.process_image(img)
