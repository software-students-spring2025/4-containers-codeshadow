from deepface import DeepFace
import base64
import cv2
import numpy as np

def readb64(base64_string):
    """Decode base64 image to OpenCV format."""
    decoded_data = base64.b64decode(base64_string.split(',')[1])
    np_data = np.frombuffer(decoded_data, np.uint8)
    return cv2.imdecode(np_data, cv2.IMREAD_COLOR)

def detect_emotion(base64_image):
    try:
        img = readb64(base64_image)
        result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
        return result[0]['dominant_emotion']
    except Exception as e:
        print("Emotion detection error:", e)
        return None

if __name__ == "__main__":
    print("This file is intended to be imported only.")