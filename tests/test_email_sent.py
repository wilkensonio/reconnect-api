import logging


def test_email_sent(client):
    email_data = {
        "email": "tcbwilkenson@gmail.com"
    }

    response = client.post("/api/v1/verify-email/", json=email_data)

    # Log response for debugging
    logging.info(f"Response from verify-email: {response.json()}")

    assert response.status_code == 200, f"Expected 200 but got {
        response.status_code}: {response.json()}"

    # Get the secret code from response
    secret_code = response.json().get('verification_code')
    assert secret_code is not None, "Expected 'verification_code' in response but got None"

    # Simulate user entering the verification code
    user_code = "123456"  # This should ideally be a dynamically generated code

    # Prepare verification data
    verify_data = {
        'user_code': user_code,
        'secret_code': secret_code
    }

    # Send request to verify email code
    response = client.post("/api/v1/verify-email-code/", json=verify_data)

    # Log response for debugging
    logging.info(f"Response from verify-email-code: {response.json()}")

    # Check if the verification was successful
    assert response.status_code == 200, f"Expected 200 but got {
        response.status_code}: {response.json()}"
