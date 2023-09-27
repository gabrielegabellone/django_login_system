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
## How to run with security settings
Another goal I set myself is to make the software safe, as if it were in production, therefore setting specific settings for a production environment, so I also created a specific docker-compose.
- To run the app with security settings:  
```docker-compose -f docker-compose-prod.yml up -d --build ```
- Check if the project is ready to be deployed  
``` docker-compose exec web python manage.py check --deploy```
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
## Resolve "Failed to exchange code for access token"
When authenticating with Google, if you POST the code to get the token and get this error message: ```{"non_field_errors":"Failed to exchange code for access token"}```, it's probably because the code received was not decoded, to fix this, I made some changes in the library:
1. go to ```venv/Lib/site-packages/dj_rest_auth/registration/serializers.py```
2. import urlib.parse at the top
```python
import urllib.parse
```
3. add this line of code in the validate method of the SocialLoginSerializer class, before the try-except block for getting the token:  
```python
code = urllib.parse.unquote(code) # add this

try:
    token = client.get_access_token(code)
except OAuth2Error as ex:
    raise serializers.ValidationError(
        _('Failed to exchange code for access token')
    ) from ex
```
