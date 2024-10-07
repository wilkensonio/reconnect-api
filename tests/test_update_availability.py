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


def test_update_availability(client, create_availability):
    valid_id = create_availability["id"]
    update_data = {
        "day": "Tuesday",
        "start_time": "09:00",
        "end_time": "18:00",
        "faculty_id": "70573522"
    }

    response = client.put(
        f"/api/v1/availability/update/{valid_id}", json=update_data)

    assert response.status_code == 200
    assert response.json()["day"] == "Tuesday"


def test_update_availability_not_found(client):
    invalid_id = 99999  # Assuming this ID does not exist
    update_data = {
        "day": "Tuesday",
        "start_time": "09:00",
        "end_time": "18:00",
        "faculty_id": "70573522"
    }

    response = client.put(
        f"/api/v1/availability/update/{invalid_id}", json=update_data)

    assert response.status_code == 404
