import pytest


def test_unregister_from_activity(client):
    """Test unregistering from an activity"""
    response = client.delete(
        "/activities/Basketball Team/unregister?email=james@mergington.edu"
    )
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]
    assert "james@mergington.edu" in data["message"]


def test_unregister_verifies_activity_exists(client):
    """Test that unregister fails for non-existent activity"""
    response = client.delete(
        "/activities/Nonexistent Activity/unregister?email=student@mergington.edu"
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_verifies_student_is_registered(client):
    """Test that unregister fails if student is not registered"""
    response = client.delete(
        "/activities/Basketball Team/unregister?email=notregistered@mergington.edu"
    )
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]


def test_unregister_removes_participant_from_activity(client):
    """Test that unregister actually removes participant from the activity"""
    # First, sign up a new participant
    email = "tempstudent@mergington.edu"
    client.post(f"/activities/Tennis Club/signup?email={email}")
    
    # Verify they were added
    activities = client.get("/activities").json()
    assert email in activities["Tennis Club"]["participants"]
    
    # Unregister
    response = client.delete(
        f"/activities/Tennis Club/unregister?email={email}"
    )
    assert response.status_code == 200
    
    # Verify they were removed
    activities = client.get("/activities").json()
    assert email not in activities["Tennis Club"]["participants"]


def test_unregister_original_participant(client):
    """Test unregistering an original participant from an activity"""
    # Verify initial state
    activities = client.get("/activities").json()
    assert "lucas@mergington.edu" in activities["Drama Club"]["participants"]
    
    # Unregister
    response = client.delete(
        "/activities/Drama Club/unregister?email=lucas@mergington.edu"
    )
    assert response.status_code == 200
    
    # Verify removal
    activities = client.get("/activities").json()
    assert "lucas@mergington.edu" not in activities["Drama Club"]["participants"]
    # Other participant should still be there
    assert "isabella@mergington.edu" in activities["Drama Club"]["participants"]
