from datetime import datetime


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
    assert response.json()[
        "email"] == "john.doe@example.com", "Email returned does not match the expected email"

    # Test that the user is already registered
    response = client.post("/api/v1/signup/", json=user_data)
    assert response.status_code == 400
    assert response.json()[
        "detail"] == "Email already registered", "Expected error message for already registered email"

    # get the user by email
    response = client.get("/api/v1/user/email/john.doe@example.com")
    assert response.status_code == 200
    assert response.json()[
        "email"] == "john.doe@example.com", "Email returned does not match the expected email"

    # get all users

    current_date = datetime.now().strftime("%B %d, %Y")

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
            "created_at": current_date
        }
    ], "Fetched user list does not match the expected user list"

    # get the user by id
    response = client.get("/api/v1/user/id/70573536")
    assert response.status_code == 200
    assert response.json()[
        "user_id"] == "70573536", "User ID returned does not match the expected user ID"
