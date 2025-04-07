"""Flask app to render the index page."""
from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def index():
    """Render the homepage."""
    return render_template('index.html')
if __name__ == "__main__":
    app.run(debug=True)

