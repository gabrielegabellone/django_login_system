# Django Login System
Project with the aim of learning how to implement an authentication system with Django Rest Framework.  
The project is structured in one app, ```authentication```, which contains the authentication logics.  
The idea is to be able to authenticate a user via username and password provided during registration or via OAuth authentication (currently, only with Google).
In both cases it is token based, so during the authentication phase an authorization token is issued which is stored in the database.  
To do this I used the ```dj-rest-auth``` and ```allauth``` packages.  
## How to install
- create a .env file and set the following variables: 
  - ```SECRET_KEY```: it is a cryptographic key, used for example to generate tokens.
  - ```GOOGLE_LOGIN_CALLBACK_URL```: is a redirect URI that you authorized when you created the OAuth credentials through Google.
- install the requirements  
```pip install requirements.txt```
- run migrations  
```python manage.py migrate```
- run the app  
```python manage.py runserver```
## API Documentation
To see the API documentation with swagger UI and test the API go to http://localhost:8000/swagger, or you can go to http://localhost:8000/swagger.json to see it in json format.