import asyncio

from ImageProcessingAgent import ImageProcessingAgent

model_paths = {
            'face_proto': 'deployproto.prototxt',
            'face_model': 'res10_300x300_ssd_iter_140000_fp16.caffemodel',
            'age_proto': 'deploy_age.prototxt',
            'age_model': 'age_net.caffemodel',
            'gender_proto': 'deploy_gender.prototxt',
            'gender_model': 'gender_net.caffemodel',
        }
async def main():
    imageAgent = ImageProcessingAgent(model_paths,"advisage_image_processing@localhost", "AdVisage_Image_Processing_Pwd")
    await imageAgent.start()
asyncio.run(main())
