def test_create_availability(client):
    availability_data = {
        "day": "Monday",
        "start_time": "08:00",
        "end_time": "17:00",
        "user_id": "70573522"
    }

    response = client.post(
        "/api/v1/availability/create/", json=availability_data)

    assert response.status_code == 200, f"Expected 200 but got {
        response.status_code}: {response.json()}"

    assert response.json()["day"] == "Monday"
    assert response.json()["start_time"] == "08:00"
    assert response.json()["end_time"] == "17:00"


def test_create_availability_invalid_data(client):
    # Test with missing required fields
    response = client.post("/api/v1/availability/create/", json={})

    assert response.status_code == 422  # Unprocessable Entity
