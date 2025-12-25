import pytest


def test_get_activities(client):
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    
    # Check that we have the expected activities
    assert "Basketball Team" in data
    assert "Tennis Club" in data
    assert "Art Studio" in data
    assert len(data) == 9


def test_get_activity_structure(client):
    """Test that activity data has the expected structure"""
    response = client.get("/activities")
    data = response.json()
    
    activity = data["Basketball Team"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_get_activities_with_participants(client):
    """Test that activities contain initial participants"""
    response = client.get("/activities")
    data = response.json()
    
    # Check Basketball Team has initial participant
    assert "james@mergington.edu" in data["Basketball Team"]["participants"]
    
    # Check Drama Club has multiple participants
    drama = data["Drama Club"]
    assert "lucas@mergington.edu" in drama["participants"]
    assert "isabella@mergington.edu" in drama["participants"]
    assert len(drama["participants"]) == 2
