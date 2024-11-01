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


def test_pi_get_msg(client, user_signup):
    msg_data = {
        "user_id": "70573536",
        "duration": 15,
        "duration_unit": "seconds",
        "message": "testing "
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

    faculty_id = user_signup["user_id"]

    response = client.put(f"/api/v1/pi-message/update/{faculty_id}",
                          json=msg_data, headers=headers)
    response_json = response.json()
    assert response.status_code == 200, 'Message updated'
    assert response_json["message"] == msg_data['message']

    response = client.get(f"/api/v1/pi-message/get/{faculty_id}",
                          headers=headers)
    response_json = response.json()
    assert response.status_code == 200, 'Message retrieved'
    assert response_json["message"] == msg_data['message']

    response = client.get(f"/api/v1/pi-message/get/70573531",
                          headers=headers)
    assert response.status_code == 400, 'Faculty not found'
