def test_email_sent(client):
    email_data = {
        "email": "reconnect980@gmail.com"
    }
    response = client.post("/api/v1/verify-email/", json=email_data)
    assert response.status_code == 200
    # Now, simulate getting user_code and secret_code
    user_code = "123456"  # This should be dynamically generated in a real scenario
    # Adjust based on actual response
    secret_code = response.json().get('verification_code')

    verify_data = {
        'user_code': user_code,
        'secret_code': secret_code
    }
    response = client.post("/api/v1/verify-email-code/", json=verify_data)

    assert response.status_code == 200
