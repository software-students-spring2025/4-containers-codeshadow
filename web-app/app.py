"""Main Flask application for the emotion detection web app."""

import os
import sys
from datetime import datetime
import requests
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
)
import flask_login
from flask_login import current_user
import pymongo
import certifi
from bson.objectid import ObjectId
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "devkey")

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DBNAME")]
users = db.users
emotions = db.Emotions
last_emotion = {"emotion": None, "start_time": datetime.utcnow()}

# Configure CORS to allow access from localhost
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5000", "http://127.0.0.1:5000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})


@app.route("/", methods=["GET", "POST"])
def login():
    """Login function to allow entry to users who have an account or need to sign up"""
    # Check if any users exist, if not create a default user
    if users.count_documents({}) == 0:
        default_user = {
            "username": "admin",
            "password": "admin123",  # In a real app, this should be hashed
            "email": "admin@example.com"
        }
        users.insert_one(default_user)
        print("Created default user: admin/admin123")

    if request.method == "POST":
        username = request.form.get("username")
        entered_pw = request.form.get("password")

        if not username or not entered_pw:
            flash("Please enter both username and password")
            return redirect(url_for("login"))

        user = users.find_one({"username": username})
        if user and user["password"] == entered_pw:
            user_obj = User(user)
            flask_login.login_user(user_obj)
            return redirect(url_for("index"))

        flash("Invalid username or password")
    return render_template("login.html")


@app.route("/index")
def index():
    """Render the homepage."""
    user_doc = users.find_one({"username": current_user.username})
    if not user_doc:
        flash("User not found", "danger")
        return redirect(url_for("login"))

    # Get the most recent emotion detected
    current_emotion = last_emotion["emotion"]

    # Get the emoji for that emotion
    emotion_doc = emotions.find_one({"Name": current_user.username})
    emoji = (
        emotion_doc.get(current_emotion, "🤔")
        if emotion_doc and current_emotion
        else "🤔"
    )

    return render_template("index.html", emoji=emoji)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Create an account"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Username and password are required", "danger")
            return redirect(url_for("signup"))

        existing_user = users.find_one(
            {"username": username}
        )  # Check if user already exists
        if existing_user:
            flash("Username already taken", "warning")
            return redirect(url_for("signup"))

        users.insert_one(
            {"username": username, "password": password}  # Insert new user
        )

        user_doc = users.find_one({"username": username})  # fetch the user again
        user = User(user_doc)
        flask_login.login_user(user)
        session["user"] = user.id

        ensure_emotion_data_for_user(username)

        flash("Signup successful!", "success")
        return redirect(url_for("index"))

    return render_template("signup.html")


@app.route("/submit-image", methods=["POST"])
def submit_image():
    """Handle image submission, analyze emotion, and return the result."""
    data = request.get_json()
    base64_img = data.get("image")

    if not base64_img:
        return jsonify({"error": "No image provided"}), 400

    try:
        response = requests.post(
            'http://ml:6000/detect',
            json={'image': base64_img}
        )
        response.raise_for_status()
        result = response.json()
        emotion = result.get('emotion')
    except Exception as e:
        print(f"Error detecting emotion: {e}")
        return jsonify({"emotion": "unknown", "emoji": "🤔"})

    if emotion:
        # Get the emoji from the DB (or fallback to mapping)
        emoji_doc = emotions.find_one({"Name": current_user.username})
        emoji = emoji_doc.get(emotion, DEFAULT_EMOTION_DATA.get(emotion, "🤔")) if emoji_doc else "🤔"

        # Update emotion count in DB
        emotions.update_one(
            {"Name": current_user.username},
            {"$inc": {f"{emotion}_count": 1}},
            upsert=True,
        )

        return jsonify({"emotion": emotion, "emoji": emoji})

    return jsonify({"emotion": "unknown", "emoji": "🤔"})


@app.route("/track")
def track():
    """Render the emotion tracker page for the logged-in user."""
    # Get the user data from the database
    emotion_doc = emotions.find_one({"Name": current_user.username})

    if not emotion_doc:
        flash("Emotion data not found for the user.", "danger")
        return redirect(url_for("index"))

    # Prepare the data to display on the tracker page
    emotion_summary = {
        "angry": emotion_doc.get("anger_count", 0),
        "disgust": emotion_doc.get("disgust_count", 0),
        "fear": emotion_doc.get("fear_count", 0),
        "happy": emotion_doc.get("happy_count", 0),
        "neutral": emotion_doc.get("neutral_count", 0),
        "sad": emotion_doc.get("sad_count", 0),
        "surprise": emotion_doc.get("surprise_count", 0),
    }
    # Render the tracker page and pass the emotion summary data
    return render_template("tracker.html", emotion_summary=emotion_summary)


DEFAULT_EMOTION_DATA = {
    "angry": "😡",
    "disgust": "🤢",
    "fear": "😖",
    "happy": "😂",
    "neutral": "😑",
    "sad": "🥲",
    "surprise": "😱",
    "angry_count": 0,
    "disgust_count": 0,
    "fear_count": 0,
    "happy_count": 0,
    "neutral_count": 0,
    "sad_count": 0,
    "surprise_count": 0,
}


def ensure_emotion_data_for_user(username):
    """Ensure the user has an emotion document in the emotions collection."""
    emotion_doc = emotions.find_one({"Name": username})
    if not emotion_doc:
        emotions.insert_one({"Name": username, **DEFAULT_EMOTION_DATA})


class User(flask_login.UserMixin):
    """User class to maintain security and usage information across different accounts"""

    def __init__(self, user_doc):
        self.id = str(user_doc["_id"])
        self.username = user_doc["username"]
        self.password = user_doc["password"]

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


@login_manager.user_loader
def user_loader(user_id):
    """Loads the user if they exist"""
    user_doc = users.find_one({"_id": ObjectId(user_id)})
    if not user_doc:
        return None
    return User(user_doc)


@login_manager.request_loader
def request_loader(req):
    """Requests to load a user if they exist"""
    username = req.form.get("username")

    if not username:
        return None
    user_doc = users.find_one({"username": username})

    if not user_doc:  # user doesn't exist
        return None
    return User(user_doc)

@app.route('/detect', methods=['POST'])
def detect():
    """Handle image upload and emotion detection."""
    if 'image' not in request.files:
        print("No image key in request.files")
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    if not image_file:
        print("Image file is empty")
        return jsonify({'error': 'Empty image file'}), 400

    try:
        image_data = image_file.read()
        print(f"Received image bytes: {len(image_data)}")

        base64_image = base64.b64encode(image_data).decode('utf-8')
        base64_image = f"data:image/jpeg;base64,{base64_image}"

        emotion = detect_emotion(base64_image)
        print("Detected emotion:", emotion)

        if emotion:
            return jsonify({'emotion': emotion})
        return jsonify({'error': 'Could not detect emotion'}), 400
    except Exception as e:
        print("Unexpected error in /detect:", e)
        return jsonify({'error': str(e)}), 500

def detect_emotion(base64_image):
    """Detect emotion by sending base64 image to the ML container."""
    try:
        response = requests.post(
            'http://ml:6000/detect',
            json={'image': base64_image},
            timeout=10
        )
        response.raise_for_status()
        return response.json().get('emotion')
    except Exception as e:
        print(f"Error detecting emotion: {e}")
        return None


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
