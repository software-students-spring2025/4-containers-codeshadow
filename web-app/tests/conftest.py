import pytest
from app import app as flask_app  

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
        "LOGIN_DISABLED": False
    })
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()

#python -m pytest tests/test_web_app.py 
#runs the test cases 