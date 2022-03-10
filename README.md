THE MOVIE REST API
===
This API is developed with DRF and use JWT for user authentication

Description
=======
The API can be executed with docker-compose. It has the following services:

- app: The main django app, it migrates the database when the service starts and create a superuser.
- db: The mysql database for the app.

It's built with Python 3.9 and Django 4.0

Docker services for development
=========
The app services runs in 8000 port
```
    # Run all services
    docker-compose up --build -d
``` 

API documentation
=========
The API documentation can be found in http://127.0.0.1:8000/docs/ or http://127.0.0.1:8000/swagger/

Before creating Movies and Persons it's necessary to create a reward for M (Movie) and P (Person). 

After it, a ProfileReward is created everytime a Movie or Person through signals.

In order to relate Movie with Person is necesary to create a Role.

