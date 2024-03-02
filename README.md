# Django CSV Parser
Parsing CSV files with best practices using django and django rest framework. We demontrate the two ways of parsing csv file with django via `django commands` and via `API`.

# Project Structure
The project structure help us to understand the project itself better. We're not focusing only coding we also should focus the project structure and the documentation.

Here is the typical top-level directory layout four our project:
    
    ├── compose          # compose folder contains necessary Dockerfiles.
    |   ├── django       # contains app dockerfile for django.
    |   ├── postgres     # contains db dockerfile for db service.
    ├── envs             # contains all env files used by our project.
    ├── src              # contains all source files (`project folder`, `apps` etc.)
    |   |── applications # contains all django's apps.
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