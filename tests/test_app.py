import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200 or response.status_code == 307
    # Should redirect to /static/index.html or serve it
    assert "text/html" in response.headers.get("content-type", "")

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)

def test_signup_and_unregister():
    # Get an activity name
    response = client.get("/activities")
    activities = response.json()
    assert activities
    activity_name = list(activities.keys())[0]
    email = "pytestuser@mergington.edu"

    # Sign up
    signup = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup.status_code == 200
    assert "Signed up" in signup.json().get("message", "")

    # Unregister
    unregister = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert unregister.status_code == 200
    assert "Unregistered" in unregister.json().get("message", "")
