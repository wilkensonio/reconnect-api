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


def test_make_app(client, user_signup):
    app_data = {
        "faculty_id": "70573522",
        "date": "2022-01-01",
        "start_time": "08:00",
        "end_time": "17:00",
        "reason": "Meeting with students",
        "status": "cancelled",
        "student_id": "70573522"
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

    response = client.post("/api/v1/appointment/create/",
                           json=app_data, headers=headers)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["reason"] == "Meeting with students"
    assert response_json["faculty_id"] == "70573522"
    assert response_json["student_id"] == "70573522"
    assert "id" in response_json
