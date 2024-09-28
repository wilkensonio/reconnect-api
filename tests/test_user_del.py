def test_del_user(client):
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

    #  Delete user by email
    response = client.delete("/api/v1/user/delete/john.doe@example.com")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}

    response = client.post("/api/v1/signup/", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == "john.doe@example.com"

    # Delete user by user_id
    response = client.delete("/api/v1/user/delete/70573536")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}

    response = client.post("/api/v1/signup/", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == "john.doe@example.com"

    # Delete user by user_id
    response = client.delete("/api/v1/user/delete/")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}

    response = client.delete("/api/v1/user/delete/123456")
    assert response.status_code == 400
    assert response.json() == {
        'detail': 'An error occurred while attempting to delete user'}
