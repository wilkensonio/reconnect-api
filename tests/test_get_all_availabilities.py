def test_get_all_availabilities(client):
    response = client.get("/api/v1/availabilities/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Should return a list
