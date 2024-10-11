def test_update_appointment(client):
    app_data = {
        "faculty_id": "70573522",
        "date": "2022-01-01",
        "start_time": "08:00",
        "end_time": "17:00",
        "reason": "Meeting with students",
        "student_id": "70573522"
    }
    response = client.post("/api/v1/appointment/create/", json=app_data)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["reason"] == "Meeting with students"
    assert response_json["faculty_id"] == "70573522"
    assert response_json["student_id"] == "70573522"
    assert "id" in response_json

    update_data = {
        "faculty_id": "70573522",
        "date": "2022-01-01",
        "start_time": "18:30",
        "end_time": "19:00",
        "reason": "Meeting with students",
        "student_id": "70573522"
    }

    response = client.put(
        f"/api/v1/appointment/update/{response_json['id']}", json=update_data)

    assert response.status_code == 200
