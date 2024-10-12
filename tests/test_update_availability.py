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
    assert "access_token" in response_json, "Access token not found in response"

    headers = {
        'Authorization': f"Bearer {response_json['access_token']}"
    }

    response = client.post(
        "/api/v1/availability/create/", json=availability_data, headers=headers)
    assert response.status_code == 200, f"Expected 200 but got {
        response.status_code}: {response.json()}"
    print("Response from create availability:", response.json())

    return response.json()


def test_update_availability(client, create_availability, user_signup):

    valid_id = create_availability["id"]
    update_data = {
        "day": "Tuesday",
        "start_time": "09:00",
        "end_time": "18:00",
        "faculty_id": "70573522"
    }
    login_data = {
        "username": user_signup["email"],
        "password": "secret_password"
    }
    response = client.post("/api/v1/token/", data=login_data)
    assert response.status_code == 200, f"Token creation failed {
        response.json()}"
    response_json = response.json()

    assert "access_token" in response_json, "Access token not found in response"

    headers = {
        'Authorization': f"Bearer {response_json['access_token']}"
    }

    response = client.put(
        f"/api/v1/availability/update/{valid_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["day"] == "Tuesday"

    # assuming that id 99999999 does not exist
    response = client.put(
        f"/api/v1/availability/update/{99999999}", json=update_data, headers=headers)
    assert response.status_code == 404, f"Expected 400 but got {
        response.status_code}: {response.json()}"
