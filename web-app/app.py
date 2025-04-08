"""Flask app to render the index page."""
from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
#from fer import FER
import base64
from pymongo import MongoClient

app = Flask(__name__)


client = MongoClient("mongodb+srv://jw7677:DuoDice2@clusterduo.zb9st.mongodb.net/?retryWrites=true&w=majority&appName=ClusterDuo")
db= client["CodeShadow"]
collection1= db["Emotions"]
@app.route("/")
def index():
    emotions= list(collection1.find())
    """Render the homepage."""
    return render_template('index.html', emotions=emotions)

@app.route('/chart')
def chart():
    return render_template('chart.html')



if __name__ == "__main__":
    app.run(debug=True)
