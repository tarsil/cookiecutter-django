# Announcement

After almost 10 years maintining this cookiecutter and with joy doing it so, it's now the time to retire it.

The painful reason behind it has nothing toon  with Django but bigger projects came out since its inception like [Dymmond](https://github.com/dymmond) and my focus has shifted towards it and my time became constrained.

I'm also the creator of:

* [Esmerald](https://esmerald.dev)
* [Lilya](https://lilya.dev)
* [AsyncMQ](https://asyncmq.dymmond.com)

And many others that require special dedicated attention and maintenance.

I would personally invite you to join me there and help growing them.

I also personally thank you for the support and for using this great cookiecutter that was also my first biggest open source contribution back in the day.

# Cookiecutter Django with PostGres + Docker + DramatiQ and optional APScheduler

![CI](https://github.com/tarsil/cookiecutter-django/actions/workflows/main.yml/badge.svg)

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

Every time a new django project needs to be set, a lot of settings and configurations need to be
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
