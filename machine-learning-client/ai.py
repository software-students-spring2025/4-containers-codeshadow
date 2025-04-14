"""Emotion detection module using DeepFace and OpenCV."""
import base64
from flask import Flask, request, jsonify
from deepface import DeepFace
import cv2  # pylint: disable=no-member
import numpy as np

app = Flask(__name__)

def readb64(base64_string):
    """Decode base64 image to OpenCV format."""
    decoded_data = base64.b64decode(base64_string.split(",")[1])
    np_data = np.frombuffer(decoded_data, np.uint8)
    return cv2.imdecode(np_data, cv2.IMREAD_COLOR)  # pylint: disable=no-member

def detect_emotion(base64_image):
    try:
        img = readb64(base64_image)
        result = DeepFace.analyze(img, actions=["emotion"], enforce_detection=False)
        print("DeepFace result:", result)
        if not result or not isinstance(result, list):
            print("No face detected")
            return None
        
        return result[0]["dominant_emotion"]
    except Exception as e:
        print("Emotion detection error:", e)
        return None

@app.route('/detect', methods=['POST'])
def detect():
    """Handle base64 image input and return detected emotion."""
    data = request.get_json()
    base64_image = data.get('image')

    if not base64_image:
        print("No image in request")
        return jsonify({'error': 'No image provided'}), 400

    emotion = detect_emotion(base64_image)
    print("Detected emotion:", emotion)

    if emotion:
        return jsonify({'emotion': emotion})
    return jsonify({'error': 'Could not detect emotion'}), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000)
