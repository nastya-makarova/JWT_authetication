# Develop a RESTful API for Authentication

## Project Description
Develop a REST API for a user authentication and authorization system using Django and Django REST Framework. The system should support user registration, authentication, token refresh, logout, and allow users to retrieve and update their personal information.

Authentication should utilize Access and Refresh tokens.

Refresh Token – A UUID stored in the database, issued for 30 days by default.
Access Token – A JSON Web Token with a default lifespan of 30 seconds.

Clients may request an Access Token refresh at any time, for instance, upon Access Token expiry by providing a valid Refresh Token. In this case, the service returns a new valid pair of Access and Refresh Tokens, resetting their lifespans.

## Installation

### Clone the repository and change the directory:

```git@github.com:nastya-makarova/JWT_authetication.git```

```cd auth_project```

### Create and activate the virtual environment::

```python3 -m venv env```

```source env/bin/activate```

### Install dependencies from the requirements.txt:

```pip install -r requirements.txt```

### Make the migrations:

```python manage.py migrate```

### Run the project:

```python manage.py runserver```


### The API documentation is available:

```http://127.0.0.1:8000/redoc/```

```http://127.0.0.1:8000/swagger/```
