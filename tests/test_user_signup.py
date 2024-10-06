def test_user_signup(client):
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
