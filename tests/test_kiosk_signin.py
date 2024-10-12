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
def std_signup(client, user_signup):
    student_data = {
        "student_id": "705735368",
        "first_name": "John",
        "last_name": "Doe",
        "email": "student.doe@southernct.edu",
        "phone_number": "1234567890"
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

    response = client.post("/api/v1/signup-student/",
                           json=student_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "student.doe@southernct.edu"
    return response.json()  # Return the created student record


def test_kiosk_signin(client, std_signup):

    login_data = {
        "user_id": std_signup['student_id']
    }

    response = client.post("/api/v1/kiosk-signin/", json=login_data)

    assert response.status_code == 200

    assert response.status_code == 200, f"Full ID : Expected 200 but got {
        response.status_code}: {response.json()}"

    last_four_id = std_signup['student_id'][-4:]

    login_data = {
        "user_id": last_four_id
    }

    response = client.post("/api/v1/kiosk-signin/", json=login_data)

    assert response.status_code == 200, f"Last_ID : Expected 200 but got {
        response.status_code}: {response.json()}"

    # Check for invalid user ID
    invalid_login_data = {
        "user_id": "9999"  # invalid ID
    }

    invalid_response = client.post(
        "/api/v1/kiosk-signin/", json=invalid_login_data)
    assert invalid_response.status_code == 400
    assert invalid_response.json(
    )["detail"] == "No User exists with the provided ID"
