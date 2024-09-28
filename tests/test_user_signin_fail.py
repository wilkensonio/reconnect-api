def test_login_user_invalid_email(client):
    # First, create a user
    user_data = {
        "user_id": "70573536",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@examplee.com",
        "password": "secret_password",
        "phone_number": "2036908924"
    }
    client.post("/api/v1/signup/", json=user_data)

    # Then, attempt to log in
    login_data = {
        "email": "john.diffemail@example.com",
        "password": "secret_password"
    }

    response = client.post("/api/v1/signin/", json=login_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "User not found"
