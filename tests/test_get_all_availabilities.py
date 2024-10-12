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


def test_get_all_availabilities(client, user_signup):
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
    response = client.get("/api/v1/availabilities/", headers=headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Should return a list
