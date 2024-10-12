
def test_valid_token(client):
    sigup_user = {
        "user_id": "70573536",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@southernct.edu",
        "password": "secret_password",
        "phone_number": "2036908924"
    }
    response = client.post("/api/v1/signup/", json=sigup_user)
    assert response.status_code == 200, f"User signup failed {
        response.json()}"

    login_data = {
        "username": sigup_user["email"],
        "password": sigup_user["password"]
    }
    response = client.post("/api/v1/token", data=login_data)
    assert response.status_code == 200, f"Token creation failed {
        response.json()}"
    response_json = response.json()
    assert "access_token" in response_json, "Access token not found in response"
    assert response_json["token_type"] == "Bearer", "Token type is not Bearer"
    assert response_json["access_token"]
