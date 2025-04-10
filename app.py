from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "machine-learning-client"))
import ai

last_emotion = {"emotion": None, "start_time": datetime.utcnow()}

app = Flask(
    __name__,
    template_folder=os.path.join("web-app", "templates"),
    static_folder=os.path.join("web-app", "static")
)

CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit-image", methods=["POST"])
def submit_image():
    data = request.get_json()
    base64_img = data.get("image")

    emotion = ai.detect_emotion(base64_img)
    
    if emotion and emotion != last_emotion["emotion"]:
        duration = (datetime.utcnow() - last_emotion["start_time"]).total_seconds()
        print(f"[{datetime.utcnow()}] Emotion changed from {last_emotion['emotion']} to {emotion} (lasted {duration} seconds)")
        last_emotion["emotion"] = emotion
        last_emotion["start_time"] = datetime.utcnow()

    return jsonify({"emotion": emotion})

if __name__ == "__main__":
    app.run(debug=True)
