import pytest


@pytest.fixture
def user_signup(client):
    user_data = {
        "user_id": "70573536",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@southernct.edu",
        "password": "secret_password",
        "phone_number": "2036908924"
    }

    response = client.post("/api/v1/signup/", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == "john.doe@southernct.edu"
    return response.json()


def test_create_availability(client, user_signup):
    availability_data = {
        "day": "Monday",
        "start_time": "08:00",
        "end_time": "17:00",
        "user_id": "70573522"
    }

    login_data = {
        "username": user_signup["email"],
        "password": "secret_password"
    }

    response = client.post("/api/v1/token/", data=login_data)
    assert response.status_code == 200
    response_json = response.json()

    headers = {
        'Authorization': f"Bearer {response_json['access_token']}"
    }

    response = client.post(
        "/api/v1/availability/create/",
        json=availability_data,
        headers=headers
    )
    assert response.status_code == 200, f"Expected 200 but got {
        response.status_code}: {response.json()}"

    assert response.json()["day"] == "Monday"
    assert response.json()["start_time"] == "08:00"
    assert response.json()["end_time"] == "17:00"

    # If data is not provided, it should return 422
    response = client.post("/api/v1/availability/create/",
                           json={}, headers=headers)
    assert response.status_code == 422  # Unprocessable Entity
