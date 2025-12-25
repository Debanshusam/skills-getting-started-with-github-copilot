import pytest


def test_signup_for_activity(client):
    """Test signing up for an activity"""
    response = client.post(
        "/activities/Basketball Team/signup?email=newstudent@mergington.edu"
    )
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    assert "newstudent@mergington.edu" in data["message"]
    assert "Basketball Team" in data["message"]


def test_signup_verifies_activity_exists(client):
    """Test that signup fails for non-existent activity"""
    response = client.post(
        "/activities/Nonexistent Activity/signup?email=student@mergington.edu"
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_prevents_duplicate_registration(client):
    """Test that a student cannot sign up twice for the same activity"""
    # Try to sign up with an email that's already registered
    response = client.post(
        "/activities/Basketball Team/signup?email=james@mergington.edu"
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_adds_participant_to_activity(client):
    """Test that signup actually adds participant to the activity"""
    email = "testnewstudent@mergington.edu"
    
    # Sign up
    response = client.post(
        f"/activities/Tennis Club/signup?email={email}"
    )
    assert response.status_code == 200
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities["Tennis Club"]["participants"]


def test_signup_multiple_participants_for_same_activity(client):
    """Test signing up multiple different participants for the same activity"""
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    
    # Sign up first student
    response1 = client.post(f"/activities/Art Studio/signup?email={email1}")
    assert response1.status_code == 200
    
    # Sign up second student
    response2 = client.post(f"/activities/Art Studio/signup?email={email2}")
    assert response2.status_code == 200
    
    # Verify both were added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email1 in activities["Art Studio"]["participants"]
    assert email2 in activities["Art Studio"]["participants"]
