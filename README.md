# Django CSV Parser
Parsing CSV files with best practices using django and django rest framework. We demontrate the two ways of parsing csv file with via `API`.

# Project Structure
The project structure help us to understand the project itself better. We're not focusing only coding we also should focus the project structure and the documentation.

Here is the typical top-level directory layout four our project:
    
    ├── compose          # compose folder contains necessary Dockerfiles.
    |   ├── django       # contains app dockerfile for django.
    |   ├── postgres     # contains db dockerfile for db service.
    ├── envs             # contains all env files used by our project.
    ├── src              # contains all source files (`project folder`, `apps` etc.)
    |   |── applications # contains all project's apps.
    └── README.md        # contains all information about the project.

# Used Techs
This project uses below techs & libraries to enchance performance and rapid development as well as best practices.
- Docker
- Pytest
- Celery
- Github Actions
- Redis ( may use dragonfly to improve caching performance )
- Logging
- Realworld project structure.

# How I Setup Project
To setup project initially i ran below command:
- django-admin startproject prj

Then i created my first app with below command:
- python manage.py startapp core

Then i created necessary docker compose files and dockerfiles to dockerize my project. Then i could build my dockerized project with below command:
- docker compose build

Then i simply run my project with below command:
- docker compose up

# Running Tests
You can run the unit tests with below commands firstly we should connect our docker container:
- docker exec -it csvparser-web-2 bash

Then we can run the unit tests with below commands:
- python manage.py test

OR

- pytest -s applications/core/tests.py