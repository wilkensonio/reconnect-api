def test_user_signup(client):
    user_data = {
        "user_id": "70573536",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "secret_password",
        "phone_number": "2036908924"
    }

    response = client.post("/api/v1/signup/", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == "john.doe@example.com"

    # Test that the user is already registered
    response = client.post("/api/v1/signup/", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

    # get the user by email
    response = client.get("/api/v1/user/email/john.doe@example.com")
    assert response.status_code == 200
    assert response.json()["email"] == "john.doe@example.com"

    # get all users
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "user_id": "70573536",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone_number": "2036908924",
            "created_at": "September 27, 2024"
        }
    ]

    # get the user by id
    response = client.get("/api/v1/user/id/70573536")
    assert response.status_code == 200
    assert response.json()["user_id"] == "70573536"
