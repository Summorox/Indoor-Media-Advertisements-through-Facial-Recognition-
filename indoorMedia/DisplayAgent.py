import cv2
from paho import mqtt


class DisplayAgent:
    def __init__(self):
        pass

    def display_image(self, img_path):
        img = cv2.imread(img_path)
        cv2.imshow('Advertisement', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def display_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        # Calculate delay between frames based on video's frame rate
        fps = cap.get(cv2.CAP_PROP_FPS)
        delay = int(1000 / fps) if fps > 0 else 25

        while (cap.isOpened()):
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow('Advertisement', frame)
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()