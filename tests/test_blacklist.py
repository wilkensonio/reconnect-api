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


def test_blacklist_user_by_id(client, user_signup):
    """Test adding a user to the blacklist."""
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
        f"/api/v1/blacklist/{user_signup['id']}",
        headers=headers
    )
    assert response.status_code == 200, "Failed to blacklist user"

    response = client.get('/api/v1/blacklist/', headers=headers)
    assert response.status_code == 200, "Failed to get blacklist"
