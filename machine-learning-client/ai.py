"""Emotion detection module using DeepFace and OpenCV."""
import base64
from deepface import DeepFace
import cv2  # pylint: disable=no-member
import numpy as np

def readb64(base64_string):
    """Decode base64 image to OpenCV format."""
    decoded_data = base64.b64decode(base64_string.split(',')[1])
    np_data = np.frombuffer(decoded_data, np.uint8)
    return cv2.imdecode(np_data, cv2.IMREAD_COLOR)  # pylint: disable=no-member

def detect_emotion(base64_image):
    """Detects the dominant emotion in a base64-encoded image using DeepFace."""
    try:
        img = readb64(base64_image)
        result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
        return result[0]['dominant_emotion']
    except Exception as e:
        print("Emotion detection error:", e)
        return None

if __name__ == "__main__":
    print("This file is intended to be imported only.")
