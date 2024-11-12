# ReConnect

**Office Hours Communication System** (API)

A communication tool for faculty to update students about office hour changes, displayed on LED screens outside offices. 

---

## Table of Contents 
- [Installation](#installation)
- [Usage](#usage)
- [Contributors](#contributors)

---

## Installation  

[Dashboard Setup](https://github.com/wilkensonio/reconnect-client)

[Raspberry PI Setup](https://github.com/wilkensonio/reconnect-pi)

0. Install these tools (if not already install), if preferred to run without docker  go the step 1

    - **Docker** : https://docs.docker.com/engine/install/
    - **Python** : https://www.python.org/downloads/ 

1. Clone the repository.
   ```bash
   git clone https://github.com/wilkensonio/reconnect-api.git

2. Navigate to the root folder
    ```bash
    cd reconnect-api

3. In the root Folder

    - Create a **.env** file 
    
        - Add the following in the **.env** file

        - PRODUCTION='false' 
       
        - DB_HOST=localhost

       
        - DB_USER=root
        - DB_PASSWORD=password
        - DB_NAME=DB_name
        - DB_PORT=3306
        - ACCESS_TOKEN_EXPIRE_MINUTES=60
        - SECRET_KEY="ba5ee6d4b415233337ca8d4ffa294818"
        - ALGORITHM="HS256"  
       
        - SMTP_SERVER="smtp.gmail.com"
        - SMTP_PORT=587
        - SENDER_EMAIL="a gmail account"
        - SENDER_PASSWORD="app_password" 

        - IFTTT_KEY=b3OPNt03ywOfjA306sApW1 

        - SMS_API_KEY="5a10bc468b1c23d5efe4d507f266379bd9ee051a1mgRMs36YerkBCzp3OXqPOSLm" 

       
        - ROOT_PASSWORD="password"
        - ROOT_EMAIL="reconnect@southernct.edu"

        Gmail password must be an app_password see Gmail documentation on how to get an app password [get app_password](https://support.google.com/accounts/answer/185833?hl=en) 
    

4. Install Dependencies 
    ```bash  
    pip or pip3 install -r requirements.txt

5. If step 0 (docker install) was skip go the step 7

6. Run application
     
    - Run command : docker build -t fast .
    
        This command will build and image using the dockerfile and the image will be tag with the name fast. In the terminal verified that the image was built successfully.,

        <img width="1319" alt="Screenshot 2024-11-12 at 2 35 07 PM" src="https://github.com/user-attachments/assets/ca38f2a8-d455-427d-8b09-a184057ea73c">

    - Run command : docker run -p 8000:8000 fastapi-app

        This command will run a docker container using the docker image build from above

        Verify that the container is running in the terminal. 

        <img width="1319" alt="docker run" src="https://github.com/user-attachments/assets/313a6b54-bec4-4f9a-a512-b7f414b573d9">

    - visit http://0.0.0.0:8000/docs
        
        Visit the URL display on the terminal from the screenshot above, maybe different from the url above.
    - API docs: base_url:8000/docs
 

7. Navigate the root directory
    - Run command : 
        ```bash
        python3 uvicorn_config.py
        ```
        or 

        ```bash
        python uvicorn_config.py
        ```


## Usage

- Signup up

    From the web browser Documentation or from the faculty dashboard create an account
    
    to use the faculty dashboard see this [setup]()

    This an exmaple from the browser. 
    - Click on the lock to the right of the endpoint and enter the apiKey in the value box, then click on authorize.
    - Click on Try it out and enter your information, user_id must be your school ID (HootlooT ID), and email must be an SCSU email (@southernct.edu).
    - Click on execute and verify the responce right below. 
    <img width="1406" alt="Screenshot 2024-11-12 at 2 51 49 PM" src="https://github.com/user-attachments/assets/02c95aa7-309a-45a6-8cce-4e525b71f91a">
    <img width="1398" alt="Screenshot 2024-11-12 at 2 52 29 PM" src="https://github.com/user-attachments/assets/93cf3f68-efaf-46ce-aee3-f18e8f3f5ba4">
    <img width="1389" alt="Screenshot 2024-11-12 at 2 52 58 PM" src="https://github.com/user-attachments/assets/bf4d6aa7-52a5-46a7-92e4-3fbaf72669dc">
    <img width="1389" alt="Screenshot 2024-11-12 at 2 53 30 PM" src="https://github.com/user-attachments/assets/ce107917-bffc-4106-b404-c7ca2da66255">

- Sign in 
    - Click on the Authorize button in the top right corner and provide an apiKey and click on authorize.
    - For username provite the SCSU email used to create the account.
    - For password provite the password entered whrn the account was created.

    - Once authorize the api can be used from the browser to make API calls and verified in the browser. 
    <img width="1406" alt="Screenshot 2024-11-12 at 2 40 42 PM" src="https://github.com/user-attachments/assets/e169d2c9-9af2-41f2-9b9e-2cae0792ca9f">
    <img width="1406" alt="Screenshot 2024-11-12 at 2 41 19 PM" src="https://github.com/user-attachments/assets/1c98e9a7-4c0e-485c-9004-ddc64e6136f6">
    <img width="1406" alt="Screenshot 2024-11-12 at 2 41 52 PM" src="https://github.com/user-attachments/assets/bd29443e-40fa-42ab-aba0-f832d63d43c8">



## Contributors

Meet the team behind the project!

- **[Wilkenson Hilarion](https://github.com/wilkensonio)**  
  Backend Developer and Full-Stack Contributor. Wilkenson built the backend, integrated IFTTT and setup CI/CD using GitHub Actions to automate the build and deployment process, conducted unit tests, and worked on the frontend, focusing on ensuring efficient communication and secure data handling.

- **[Mitchell DeCesare](https://github.com/MitchellDC)**  
  Frontend and Testing Specialist. Mitchell contributed to the faculty dashboard interface, and testing for the PI interface

- **[Escobar J.](https://github.com/Escobarj6)**  
  Pi Frontend Developer. Escobar developed the frontend interface for the Raspberry Pi, enabling clear communication and easy interaction for faculty and students. 3D print the casing to to house the PI

## Acknowledgements

Special thanks to all contributors, supporters, and resources that helped make this project possible. 

