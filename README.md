# Cookiecutter Django

[![CircleCI](https://circleci.com/gh/tarsil/cookiecutter-django.svg?style=shield&circle-token=91ae5605f46538c06c9b88248fd0fd6cc9b2994d)](https://circleci.com/gh/tarsil/cookiecutter-django)
[![Codefresh build status]( https://g.codefresh.io/api/badges/pipeline/tiagoarasilva/Django%20Cookiecutter%2FTest%26Build?type=cf-1&key=eyJhbGciOiJIUzI1NiJ9.NThhOGRkNTdmMjU5OWMwMTAwZjQzYmRi.kUnXk46L86nOtnW3OI5-TJK6cYlavAHbhF5MqKg6pLM)](https://g.codefresh.io/pipelines/edit/new/builds?id=5fc91f0654e9095fcd293333&pipeline=Test%26Build&projects=Django%20Cookiecutter&projectId=5fc91e5e84fbdc5d38bf1924)

This is a cookiecutter application that aims to help people speeding up the development process.

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
2. Python 3.8+
3. Any virtual environment at your choice

## Cookiecutter

1. Cookiecutter - More details how to use and install [here](https://cookiecutter.readthedocs.io/en/1.7.2/)

## Task Manager

This project implements [dramatiq](https://dramatiq.io/)

## Install the template

1. `cookiecutter https://github.com/tiagoarasilva/cookiecutter-django` and follow the instructions.
    **When giving a name to your project, avoid dashes by using underscores instead.**
