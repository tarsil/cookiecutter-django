# Cookiecutter Django with PostGres + Docker + DramatiQ

[![CircleCI](https://circleci.com/gh/tarsil/cookiecutter-django.svg?style=shield&circle-token=91ae5605f46538c06c9b88248fd0fd6cc9b2994d)](https://circleci.com/gh/tarsil/cookiecutter-django)
[![Codefresh build status]( https://g.codefresh.io/api/badges/pipeline/tiagoarasilva/Django%20Cookiecutter%2FTest%26Build?type=cf-1&key=eyJhbGciOiJIUzI1NiJ9.NThhOGRkNTdmMjU5OWMwMTAwZjQzYmRi.kUnXk46L86nOtnW3OI5-TJK6cYlavAHbhF5MqKg6pLM)](https://g.codefresh.io/pipelines/edit/new/builds?id=5fc91f0654e9095fcd293333&pipeline=Test%26Build&projects=Django%20Cookiecutter&projectId=5fc91e5e84fbdc5d38bf1924)

This is a cookiecutter application that aims to help people speeding up the development process.
We use [django-guardian](https://django-guardian.readthedocs.io/en/stable/) for user permissions
if not using external services (Auth0, Google...) as we see it fit and easy to use
as well as simple to manipulate complex object permissions.

## Table of Contents

- [Introduction](#introduction)
- [Requirements](#requirements)
- [Cookiecutter](#cookiecutter)
- [Task Manager](#task-manager)
- [Install the Template](#install-the-template)

---

## Introduction

Every time a new django project needs to be set a lot of settings and configurations need to be
also set and this cookiecutter offers a lot of boilerplating including:

1. Login
2. Task Manager with Dramatiq
3. Django Rest Framework
4. Redis
5. RabbitMQ
6. PGBouncer for database accesses
7. [django-guardian](https://django-guardian.readthedocs.io/en/stable/)
8. MongoDB as Optional

All of this using docker.

## Requirements

To use this cookiecutter you should have at least.

1. [Docker](https://www.docker.com/products)
2. Python 3.8
3. Any virtual environment at your choice

## Cookiecutter

1. Cookiecutter - More details how to use and install [here](https://cookiecutter.readthedocs.io/en/latest/)

## Task Manager

This project implements [dramatiq](https://dramatiq.io/)

The project also contains inside the `development/settings.py` a `DRAMATIQ_BROKER` specially
designed for developement. For users used to `CELERY_TASK_ALWAYS_EAGER=True`, this broker
has a similar behaviour. Special thanks to @dnmellen for providing an alternative.

## Install the template

1. `cookiecutter https://github.com/tarsil/cookiecutter-django` and follow the instructions.
    **When giving a name to your project, avoid dashes by using underscores instead.**
