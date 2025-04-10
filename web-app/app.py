import flask
from flask import Flask, render_template, request, redirect, url_for, flash, session
import flask_login
from flask_login import current_user, login_required
import pymongo
from pymongo import MongoClient
import os
import certifi

app = Flask(__name__)

#login 
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

#mongodb client
client = pymongo.MongoClient(os.getenv("MONGO_URI"), tlsCAFile=certifi.where())
db = client[os.getenv("MONGO_DBNAME")]
users = db.users

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        existing_user = users.find_one({"username": username})
        if existing_user:
            flash("Username already exists", "danger")
            return redirect(url_for("signup")) #, "Username already exists", "danger"

        new_doc = db.users.insert_one({"username": username, "password": password})
        user_id = str(new_doc.inserted_id)
        return redirect(url_for("login")) #, message="Sign up successful! You can now log in."
    return render_template("signup.html")


@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        entered_pw = request.form.get('password')

        if not username or not entered_pw:
            flash("Username and password are required", "danger")
            return redirect(url_for("login"))
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

@app.route("/home")
@login_required
def index():
    """Render the homepage."""
    return render_template("index.html")



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