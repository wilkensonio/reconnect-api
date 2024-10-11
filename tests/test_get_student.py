def test_get_student(client):
    student_data = {
        "student_id": "705735368",
        "first_name": "John",
        "last_name": "Doe",
        "email": "hilarionw2@southernct.edu",
        "phone_number": "1234567890"
    }

    response = client.post("/api/v1/signup-student/", json=student_data)
    assert response.status_code == 200, f"Expected 200 but got {
        response.status_code}: {response.json()}"

    response = client.get("/api/v1/students/")

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
