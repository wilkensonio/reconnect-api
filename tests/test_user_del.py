def test_del_user(client):
    user_data = {
        "user_id": "70573536",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@southernct.edu",
        "password": "secret_password",
        "phone_number": "2036908924"
    }

    # Sign up user
    response = client.post("/api/v1/signup/", json=user_data)
    print(response.json())
    assert response.status_code == 200, f"fail signup: {response.json()}"
    assert response.json()["email"] == "john.doe@southernct.edu"

    # Delete user by email
    response = client.delete("/api/v1/user/delete/john.doe@southernct.edu")
    assert response.status_code == 200
    assert response.json() == {"detail": "User deleted successfully"}

    # Sign up user again to check deletion by user_id
    response = client.post("/api/v1/signup/", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == "john.doe@southernct.edu"

    # Delete user by user_id
    response = client.delete("/api/v1/user/delete/70573536")
    assert response.status_code == 200
    assert response.json() == {"detail": "User deleted successfully"}

    # Try deleting without providing user_id (404 error expected)
    response = client.delete("/api/v1/user/delete/")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}

    # Try deleting an invalid user_id (400 error expected)
    response = client.delete("/api/v1/user/delete/123456")
    assert response.status_code == 400
    assert response.json() == {
        'detail': 'An error occurred while attempting to delete user'}

    # Try deleting a user that does not exist (404 error expected)
    response = client.delete("/api/v1/delete/123456")
    assert response.status_code == 404
