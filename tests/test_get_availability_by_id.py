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


@pytest.fixture
def create_availability(client, user_signup):
    # Create a valid availability entry
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
    assert response.status_code == 200, f"Token creation failed {
        response.json()}"
    response_json = response.json()

    headers = {
        'Authorization': f"Bearer {response_json['access_token']}"
    }
    response = client.post(
        "/api/v1/availability/create/", json=availability_data, headers=headers)
    return response.json()  # Return the created availability record


def test_get_availability_by_id(client, create_availability, user_signup):
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

    valid_id = create_availability["id"]
    response = client.get(
        f"/api/v1/availability/get-by-id/{valid_id}", headers=headers)

    assert response.status_code == 200
    assert "day" in response.json()  # Assuming the response contains the 'day' field

    # Check for invalid availability ID
    invalid_id = 99999  # Assuming this ID does not exist
    response = client.get(
        f"/api/v1/availability/get-by-id/{invalid_id}", headers=headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Availability not found"
