# Cookiecutter Django

This is a cookicutter application that aims to help people speeding up the development process.

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

All of this using docker.

## Requirements

To use this cookiecutter you should have at least.

1. [Docker](https://www.docker.com/products)
2. Python 3.7+
3. Any virtual environment at your choice

## Cookicutter

1. Cookiecutter - More details how to use and install [here](https://cookiecutter.readthedocs.io/en/1.7.2/)

## Task Manager

This project implements [dramatiq](https://dramatiq.io/)

## Install the template

1. `cookiecutter https://github.com/tiagoarasilva/cookicutter-django` and follow the instructions.
    **When giving a name to your project, avoid dashes by using underscores instead.**
