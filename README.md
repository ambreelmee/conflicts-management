# Conflicts management

This micro-service is part of the backend architecture of the dataESR project.
Its purpose is to help the administrator updating the main database **dataESR** with distant source databases by dealing with conflictual cases.

## Table of Contents
1. [Dependencies](#dependencies)
1. [Getting Started](#getting-started)
1. [Commands](#commands)
1. [Database](#database)
1. [Application Structure](#application-structure)
1. [Development](#development)
1. [Testing](#testing)
1. [Lint](#lint)
1. [Swagger](#swagger)

## Dependencies

You will need [docker](https://docs.docker.com/engine/installation/) and [docker-compose](https://docs.docker.com/compose/install/).

## Getting Started

First, clone the project, install dependencies and check that it works

```bash
$ make install      # Install the pip dependencies on the docker container
$ make start        # Run the container containing your local python server
```
If everything works, you should see the available routes [here](http://127.0.0.1:3000/application/spec).


## Commands

While developing, you will probably rely mostly on `make start`; however, there are additional scripts at your disposal:

|`make <script>`|Description|
|------------------|-----------|
|`install`|Install the pip dependencies on the server's container.|
|`start`|Run your local server in its own docker container.|
|`daemon`|Run your local server in its own docker container as a daemon.|
|`db/connect`|Connect to your docker database.|
|`db/migrate`|Generate a database migration file using alembic, based on your model files.|
|`db/upgrade`|Run the migrations until your database is up to date.|
|`db/downgrade`|Downgrade your database by one migration.|
|`tests`|Run unit tests with unittest in its own container.|
|`lint`|Run flake8 on the `src` directory.|


## Application Structure


```
.
├── devops                   # Project devops configuration settings
│   └── deploy               # Environment-specific configuration files for shipit
├── migrations               # Database's migrations settings
│   └── versions             # Database's migrations versions generated by alembic
├── src                      # Application source code
│   ├── models               # Python classes modeling the database
│   │   ├── abc.py           # Abstract base class model
│   │   └── user.py          # Definition of the user model
│   ├── repositories         # Python classes allowing you to interact with your models
│   │   └── user.py          # Methods to easily handle user models
│   ├── resources            # Python classes containing the HTTP verbs of your routes
│   │   └── user.py          # Rest verbs related to the user routes
│   ├── routes               # Routes definitions and links to their associated resources
│   │   ├── __init__.py      # Contains every blueprint of your API
│   │   └── user.py          # The blueprint related to the user
│   ├── swagger              # Resources documentation
│   │   └── user             # Documentation of the user resource
│   │       └── GET.yml      # Documentation of the GET method on the user resource
│   ├── util                 # Some helpfull, non-business Python functions for your project
│   │   └── parse_params.py  # Wrapper for the resources to easily handle parameters
│   ├── config.py            # Project configuration settings
│   ├── manage.py            # Project commands
This application was generated using the boilerplate Flask Api Starter Kit created by Antoine Kahn
│   └── server.py            # Server configuration
└── test                     # Unit tests source code
```
