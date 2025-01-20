# Develop a RESTful API for Authentication

## Описание проекта
Develop a REST API for a user authentication and authorization system using Django and Django REST Framework. The system should support user registration, authentication, token refresh, logout, and allow users to retrieve and update their personal information.

Authentication should utilize Access and Refresh tokens.

Refresh Token – A UUID stored in the database, issued for 30 days by default.
Access Token – A JSON Web Token with a default lifespan of 30 seconds.

Clients may request an Access Token refresh at any time, for instance, upon Access Token expiry by providing a valid Refresh Token. In this case, the service returns a new valid pair of Access and Refresh Tokens, resetting their lifespans.

## Установка

### Клонировать репозиторий и перейти в него в командной строке:

```git@github.com:nastya-makarova/JWT_authetication.git```

```cd auth_project```

### Cоздать и активировать виртуальное окружение:

```python3 -m venv env```

```source env/bin/activate```

### Установить зависимости из файла requirements.txt:

```pip install -r requirements.txt```

### Выполнить миграции:

```python manage.py migrate```

### Запустить проект:

```python manage.py runserver```


### Документация для API Yatube доступна:

```http://127.0.0.1:8000/redoc/```

```http://127.0.0.1:8000/swagger/```
