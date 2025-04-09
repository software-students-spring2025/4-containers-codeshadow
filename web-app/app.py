"""Flask app to render the index page."""
from flask import Flask, render_template
from pymongo import MongoClient
import pprint
app = Flask(__name__)



client = MongoClient("mongodb+srv://jw7677:DuoDice2@clusterduo.zb9st.mongodb.net/?retryWrites=true&w=majority&appName=ClusterDuo")
db= client["CodeShadow"]
collection1= db["Emotions"]

@app.route("/")
def index():
    """Render the homepage."""
    return render_template("index.html")

for doc in collection1.find():
    pprint.pprint(doc)

if __name__ == "__main__":
    app.run(debug=True)
