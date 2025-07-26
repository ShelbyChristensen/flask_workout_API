import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from server.app import app, db
from server.models import Workout

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_create_valid_workout(client):
    response = client.post('/workouts', json={
        "date": "2025-07-26",
        "duration_minutes": 30,
        "notes": "Test workout"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["duration_minutes"] == 30

def test_create_invalid_workout_duration(client):
    response = client.post('/workouts', json={
        "date": "2025-07-26",
        "duration_minutes": 0,  # Invalid
        "notes": "This should fail"
    })
    assert response.status_code == 400
    assert "duration" in response.get_json()["error"].lower()
