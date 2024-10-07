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


def test_delete_availability(client, create_availability):
    valid_id = create_availability["id"]
    response = client.delete(f"/api/v1/availability/delete/{valid_id}")

    assert response.status_code == 200
    assert response.json() is True  # Should return True on successful deletion


def test_delete_availability_not_found(client, create_availability):
    invalid_id = 99999  # Assuming this ID does not exist
    response = client.delete(f"/api/v1/availability/delete/{invalid_id}")

    assert response.status_code == 404
    assert response.json()[
        "detail"] == "Availability not found or already deleted"
