import flask
from flask import Flask, render_template, request, redirect, url_for, flash, session
import flask_login
from flask_login import current_user, login_required
import pymongo
from pymongo import MongoClient
import os
import sys
import certifi
from bson.objectid import ObjectId
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
app.secret_key = os.getenv("SECRET_KEY", "devkey")

CORS(app)

#login 
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

#mongodb client
client = pymongo.MongoClient(os.getenv("MONGO_URI"), tlsCAFile=certifi.where())
db = client[os.getenv("MONGO_DBNAME")]
users = db.users

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        entered_pw = request.form.get('password')

        if not username or not entered_pw:
            flash("Username and password are required", "danger")
            return redirect(url_for("login"))

        user_doc = users.find_one({"username": username})
        if user_doc and (entered_pw == user_doc["password"]):
            user = User(user_doc)
            flask_login.login_user(user)
            session["user"] = user.id
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")
'''    
        user_doc = users.find_one({"username": username})

        if user_doc and (entered_pw == user_doc["password"]): #correct credentials
            user = User(user_doc)
            flask_login.login_user(user)
            session["user"] = user.id
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password", "danger")
            return render_template("login.html")
        '''
    #return render_template("templates/login.html")

@app.route("/index")
def index():
    """Render the homepage."""
    #print("CURRENT USER:", current_user.username)
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

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Username and password are required", "danger")
            return redirect(url_for("signup"))

        # Check if user already exists
        existing_user = users.find_one({"username": username})
        if existing_user:
            flash("Username already taken", "warning")
            return redirect(url_for("signup"))

        # Insert new user
        users.insert_one({
            "username": username,
            "password": password
        })

        # Auto-login the user and redirect to homepage
        user_doc = users.find_one({"username": username})  # fetch the user again
        user = User(user_doc)
        flask_login.login_user(user)
        session["user"] = user.id

        flash("Signup successful!", "success")
        return redirect(url_for("index"))  #this return was unreachable before

    return render_template("signup.html")

class User(flask_login.UserMixin):
    def __init__(self, user_doc):
        self.id = str(user_doc["_id"])
        self.username = user_doc["username"]
        self.password = user_doc["password"]

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.id


@login_manager.user_loader
def user_loader(user_id):
    user_doc = users.find_one({"_id": ObjectId(user_id)})
    if not user_doc:
        return
    
    return User(user_doc)


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')

    if not username:
        return
    
    user_doc = users.find_one({"username": username})

    if not user_doc: #user doesn't exist
        return None

    return User(user_doc)

if __name__ == "__main__":
    app.run(debug=True)