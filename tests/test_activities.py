"""Tests for activities endpoints using AAA (Arrange-Act-Assert) pattern."""


def test_get_activities_returns_activities(client):
    # Arrange: client fixture provides TestClient

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_adds_participant(client):
    # Arrange
    email = "tester1@mergington.edu"
    activity = "Chess Club"

    # Act
    resp = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert resp.status_code == 200
    data = client.get("/activities").json()
    assert email in data[activity]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    email = "tester2@mergington.edu"
    activity = "Programming Class"

    # first signup
    first = client.post(f"/activities/{activity}/signup?email={email}")
    assert first.status_code == 200

    # Act (duplicate)
    duplicate = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert duplicate.status_code == 400


def test_remove_participant(client):
    # Arrange
    email = "tester3@mergington.edu"
    activity = "Gym Class"
    signup = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup.status_code == 200

    # Act
    resp = client.delete(f"/activities/{activity}/participants?email={email}")

    # Assert
    assert resp.status_code == 200
    data = client.get("/activities").json()
    assert email not in data[activity]["participants"]
