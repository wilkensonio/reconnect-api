import pytest


@pytest.fixture
def create_availability(client):
    # Create a valid availability entry
    availability_data = {
        "day": "Monday",
        "start_time": "08:00",
        "end_time": "17:00",
        "user_id": "70573522"
    }

    response = client.post(
        "/api/v1/availability/create/", json=availability_data)
    return response.json()  # Return the created availability record


def test_get_availability_by_id(client, create_availability):
    # Assuming you have a valid ID in your database for testing
    valid_id = create_availability["id"]
    response = client.get(f"/api/v1/availability/get-by-id/{valid_id}")

    assert response.status_code == 200
    assert "day" in response.json()  # Assuming the response contains the 'day' field


def test_get_availability_by_id_not_found(client):
    invalid_id = 99999  # Assuming this ID does not exist
    response = client.get(f"/api/v1/availability/get-by-id/{invalid_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Availability not found"
