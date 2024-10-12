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


def test_create_student(client, user_signup):
    student_data = {
        "student_id": "705735368",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@southernct.edu",
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
    assert response.status_code == 200, f"Expected 200 but got {
        response.status_code}: {response.json()}"

    # Check if the returned student data matches the input (except password)
    assert response.json()["first_name"] == student_data["first_name"]
    assert response.json()["email"] == student_data["email"]

    # Check for invalid email address
    invalid_email_data = student_data.copy()
    invalid_email_data["email"] = "john.doe@gmail.com"

    invalid_response = client.post(
        "/api/v1/signup-student/", json=invalid_email_data, headers=headers)
    assert invalid_response.status_code == 400
    assert invalid_response.json(
    )["detail"] == "Invalid southern email address"
