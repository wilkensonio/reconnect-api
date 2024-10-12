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


def test_get_student(client, user_signup):

    student_data = {
        "student_id": "705735368",
        "first_name": "John",
        "last_name": "Doe",
        "email": "hilarionw2@southernct.edu",
        "phone_number": "1234567890"
    }
    login_data = {
        "username": user_signup["email"],
        "password": "secret_password"
    }
    response = client.post("/api/v1/token/", data=login_data)
    assert response.status_code == 200, f"Token creation failed {
        response.json()}"
    response_json = response.json()

    headers = {
        'Authorization': f"Bearer {response_json['access_token']}"
    }
    response = client.post("/api/v1/signup-student/",
                           json=student_data, headers=headers)
    assert response.status_code == 200, f"Expected 200 but got {
        response.status_code}: {response.json()}"

    response = client.get("/api/v1/students/", headers=headers)

    assert response.status_code == 200, f"Expected 200 but got {
        response.status_code}: {response.json()}"

    students = response.json()
    assert isinstance(students, list), f"Expected list but got {
        type(students)}"

    if students:
        student = students[0]
        assert "first_name" in student
        assert "last_name" in student
        assert "email" in student
