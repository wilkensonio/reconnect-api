def test_user_signin(client):
    # First, create a user
    user_data = {
        "user_id": "70573536",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@southernct.edu",
        "password": "secret_password",
        "phone_number": "2036908924"
    }
    client.post("/api/v1/signup/", json=user_data)

    # Then, attempt to log in
    login_data = {
        "email": "john.doe@southernct.edu",
        "password": "secret_password"
    }
    response = client.post("/api/v1/signin/", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Test for invalid email

    login_data = {
        "email": "john.diffemail@southernct.edu",
        "password": "secret_password"
    }

    response = client.post("/api/v1/signin/", json=login_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "User not found"
