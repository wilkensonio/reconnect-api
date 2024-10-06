def test_kiosk_signin(client):
    student_data = {
        "student_id": "705735368",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@southernct.com",
        "phone_number": "1234567890"
    }

    response = client.post("/api/v1/signup-student/", json=student_data)
    assert response.status_code == 200, f"Expected 200 but got {
        response.status_code}: {response.json()}"

    response_json = response.json()

    login_data = {
        "user_id": response_json['student_id']
    }

    response = client.post("/api/v1/kiosk-signin/", json=login_data)

    assert response.status_code == 200

    assert response.status_code == 200, f"Full ID : Expected 200 but got {
        response.status_code}: {response.json()}"

    last_four_id = response_json['student_id'][-4:]

    login_data = {
        "user_id": last_four_id
    }

    response = client.post("/api/v1/kiosk-signin/", json=login_data)

    assert response.status_code == 200, f"Last_ID : Expected 200 but got {
        response.status_code}: {response.json()}"

    # Ensure the token is returned in the response
    token_response = response.json()
    assert "access_token" in token_response
    assert token_response["token_type"] == "bearer"

    # Check for invalid user ID
    invalid_login_data = {
        "user_id": "9999"  # invalid ID
    }

    invalid_response = client.post(
        "/api/v1/kiosk-signin/", json=invalid_login_data)
    assert invalid_response.status_code == 400
    assert invalid_response.json(
    )["detail"] == "No User exists with the provided ID"
