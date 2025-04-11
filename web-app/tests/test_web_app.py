import pytest

from app import users, emotions
from bson.objectid import ObjectId

def test_login_page_loads(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"Log In" in res.data

def test_signup_and_login(client):
    client.post("/signup", data={
        "username": "testuser",
        "password": "testpass"
    }, follow_redirects=True)

    user_doc = users.find_one({"username": "testuser"})
    assert user_doc is not None

    res = client.post("/", data={
        "username": "testuser",
        "password": "testpass"
    }, follow_redirects=True)

    assert b"Welcome" in res.data

def test_missing_signup_fields(client):
    res = client.post("/signup", data={}, follow_redirects=True)
    assert b"Username and password are required" in res.data

def test_submit_image_no_data(client):
    res = client.post("/submit-image", json={}, follow_redirects=True)
    assert res.status_code == 400
    assert b"No image provided" in res.data

def test_submit_image_with_emotion(client, monkeypatch):
    username = "emotionuser"
    password = "123"
    client.post("/signup", data={"username": username, "password": password}, follow_redirects=True)

    monkeypatch.setattr("app.detect_emotion", lambda x: "happy")

    res = client.post("/submit-image", json={"image": "fakebase64img"})
    data = res.get_json()
    assert res.status_code == 200
    assert data["emotion"] == "happy"
    assert "emoji" in data

    doc = emotions.find_one({"Name": username})
    assert doc["happy_count"] > 0