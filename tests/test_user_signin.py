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


def test_user_signin(client, user_signup):
    # Test login with valid user credentials
    login_data = {
        "email": user_signup["email"],
        "password": "secret_password"
    }
    response = client.post("/api/v1/signin/", json=login_data)
    assert response.status_code == 200

    # Test for invalid email
    login_data = {
        "email": "johndoe@southernct.edu",
        "password": "secret_password"
    }

    response = client.post("/api/v1/signin/", json=login_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "User not found"
