def test_create_student(client):
    student_data = {
        "student_id": "705735368",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@southernct.edu",
        "phone_number": "1234567890"
    }
    response = client.post("/api/v1/signup-student/", json=student_data)
    assert response.status_code == 200, f"Expected 200 but got {
        response.status_code}: {response.json()}"

    # Check if the returned student data matches the input (except password)
    assert response.json()["first_name"] == student_data["first_name"]
    assert response.json()["email"] == student_data["email"]

    # Check for invalid email address
    invalid_email_data = student_data.copy()
    invalid_email_data["email"] = "john.doe@gmail.com"

    invalid_response = client.post(
        "/api/v1/signup-student/", json=invalid_email_data)
    assert invalid_response.status_code == 400
    assert invalid_response.json(
    )["detail"] == "Invalid southern email address"
