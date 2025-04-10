"""Main Flask application for the emotion detection web app."""

import os
import sys
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# Get the absolute path to the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the path to the machine-learning-client directory
sys.path.append(os.path.join(parent_dir, "machine-learning-client"))
from ai import detect_emotion

last_emotion = {"emotion": None, "start_time": datetime.utcnow()}

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

CORS(app)

@app.route("/")
def index():
    """Render the homepage."""
    return render_template("index.html")

@app.route("/submit-image", methods=["POST"])
def submit_image():
    """Handle image submission, analyze emotion, and return the result."""
    data = request.get_json()
    base64_img = data.get("image")
    emotion = detect_emotion(base64_img)
    if emotion and emotion != last_emotion["emotion"]:
        duration = (datetime.utcnow() - last_emotion["start_time"]).total_seconds()
        print(f"[{datetime.utcnow()}] {last_emotion['emotion']} to {emotion} (lasted {duration} seconds)")
        last_emotion["emotion"] = emotion
        last_emotion["start_time"] = datetime.utcnow()

    return jsonify({"emotion": emotion})

if __name__ == "__main__":
    app.run(debug=True)
