# {{ cookiecutter.project_name }}

## Table of Contents

- [Initial Notes](#initial-notes)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Docker Structure](#docker-structure)
- [Setup](#setup)
- [Start the Development Environment](#start-the-development-environment)
- [Additional Useful Commands](#additional-useful-commands)
- [Tests](#tests)

---

## Initial notes

- This project runs on Django 3.2+ and Python 3.
- The requirements are located inside the requirements folder for:
  - development
  - deployment
  - testing/staging/live

## Requirements

  1. MacOS 15+, Ubuntu 20+ or Windows WSL
  2. Virtual environment to run in isolation without breaking the system.
      - [Python venv](https://docs.python.org/3/library/venv.html)
      - [VirtualEnvWrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
  3. [Docker](https://docs.docker.com/get-docker/)
  4. IDE at your choice

---

## Installation

The way the projet was assembled was to run inside docker to avoid a lot of external tooling and to
replicate as much as possible the production environment by dockerizing it.

The command `make` will display all the options and automation of the project.

### Docker Structure

  1. db
  2. redis
  3. rabbitmq
  4. {{ cookiecutter.project_name }}
  5. pgbouncer

## Setup

The first run with the project, there are a few recommended steps to make it clean and simple.

  1. Create a new virtual environment with python 3.8+.
  2. `make requirements-dev` - Installs the requirements for development.
  3. `make start_docker` - Starts docker containers with no logs.
      1. (Optional) - `make start_docker_logs` starts docker with all logs.

The first run will ask you to create the volumes (step 3). Just follow the instructions on the screen.

## Start the Development Environment

When the project is starting for the first time, the migrations should be applied to your local.

  1. `make migrate` - Applies the migrations to your local machine.
  2. `make createsuperuser`- Create a superuser for yourself if is the first time running the project.
  3. `make run` - Starts the project.
  4. Go to `https://localhost:8000` and have fun!

### Additional Useful Commands

During the development sometimes we need to perform actions such as:

  1. Creating migrations.
  2. Test async tasks with dramatiq.
  3. Run the unittests.

For these functionalities we provide some automation to make it easier the development.

  1. `make migrations` - Creates new migrations. This command is a wrapper of the `makemigrations`
  command from django.
  2. `make dramatiq` - Starts the dramatiq workers locally.
  3. `make test` - Runs all the tests of the platform.
  4. `make shell` - Starts the shell in interactive mode.

For commands and explanations, run `make` and a list will be displayed with a small description.

## Tests

To make the life of our developers easier, we also have a wrapper to run the tests.

  1. `make test` - Runs the whole suite of tests in the platform and rebuilds always the test
  db every time it runs.
  2. `make test TESTONLY='name_of_module'` - Runs the tests for a specific module instead the
  whole codebase. This also rebuilds the DB every time it runs. Example:
      1. `make test TESTONLY='accounts'.
      2. `make test TESTONLY='accounts.tests.test_models'.
  3. `make test-reusedb`. Runs the whole suite of tests in the platform without rebuilding the db.
  4. `make test-reusedb TESTONLY='name_of_module'` -
  Same principle or `make test TESTONLY` but without rebuilding the db.