# Django Login System
![Coverage Badge](./reports/coverage-badge.svg)  
Project with the aim of learning how to implement an authentication system with Django Rest Framework.  
The project is structured in one app, **authentication**, which contains the authentication logics.  
The idea is to be able to authenticate a user via username and password provided during registration or via OAuth authentication (currently, only with Google).
In both cases it is token based, so during the authentication phase an authorization token is issued which is stored in the database.  

To do this I used the **dj-rest-auth** and **allauth** packages.
For the database I used the default **SQLite** in order to better focus on other aspects.

Any feedback or advice to improve this project is welcome 😊
## Set environment variables
Create a .env file and set the following variables: 
  - ```SECRET_KEY```: it is a cryptographic key, used for example to generate tokens.
  - ```GOOGLE_LOGIN_CALLBACK_URL```: is a redirect URI that you authorized when you created the OAuth credentials through Google.
## How to run
- install the requirements  
```pip install requirements.txt```
- run migrations  
```python manage.py migrate```
- run the app  
```python manage.py runserver```
## How to run (with Docker)
- build and run the app   
```docker-compose up```
- run migrations  
```docker-compose run web python manage.py migrate```
## API Documentation
To see the API documentation with swagger UI and test the API go to http://localhost:8000/swagger, or you can go to http://localhost:8000/swagger.json to see it in json format.
## Google Authentication
How do I authenticate a Google account?  
1. Go to ```https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=<GOOGLE_LOGIN_CALLBACK_URL>&prompt=consent&response_type=code&client_id=<YOUR CLIENT ID>&scope=openid%20email%20profile&access_type=offline``` and choose the account with which you want to authenticate.
Next, you will be redirected to this page:
<img width="500" alt="Screenshot 2023-09-23 171939" src="https://github.com/gabrielegabellone/django_login_system/assets/115152050/1d0e5d95-e9af-4f54-a534-cdaa41bd8b7f">   


2. So, go and manually grab the code provided in the URL and POST it to the Google Login enpoint:  
```curl -X POST http://localhost:8000/dj-rest-auth/google/ -H 'Content-type: application/json' -d '{"code":"<your_authorization_code>"}'```

3. Now a new user will be created in the database and you will get a token that you can use to make authorized requests:  
Request: ```curl http://localhost:8000/auth/hello/ -H 'Authorization: Token <your_token>'```  
Response: ```{"message":"Hello <username>!"}```
## Problems Encountered
### Failed to exchange code for access token
The first times I tried to authenticate with Google, I had problems getting the token through the code. I received this response: ```{"non_field_errors":"Failed to exchange code for access token"}```.  
While debugging I discovered that the cause was the following exception:  ```Error retrieving access token: b'{\n  "error": "invalid_grant",\n  "error_description": "Malformed auth code."\n}'```.  
So basically it was an authorization code decoding problem, where the `%2F` had to be encoded in `/`. So I identified 2 possible solutions:
- manually replace the ```%2F``` in ```/``` of the authorization code when you make the POST request;
- add a control directly into the library, then go to ```venv/Lib/site-packages/dj_rest_auth/registration/serializers.py``` and add this code block to line 134 (before the try-except block for getting the token):  
```python
if '%2F' in code:
    code = code.replace('%2F', '/')
```
