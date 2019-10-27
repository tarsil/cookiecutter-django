[![License: MIT](https://img.shields.io/github/license/vintasoftware/django-react-boilerplate.svg)](LICENSE.txt)

Django Docker Boilerplate - Django Rest Framework with Redis, RabbitMQ and Celery
===============================================================================

## Note

- The template is using foundation as a framework but this can be changed by your personal preference, you only need to update the references in the `static` and `templates` folder.
- Inside the views located in accounts, there are some that you need to create your own files, such as the registration or change password, the code is there, you only need to place the HTML inside the proper directory. The only HTML placed and working is the login and the homepage to allow you to do a first run.
- Comes with a bunch of plugins for many kinds of projects. Not all of them are needed, feel free to remove what you don't need
- This boilerplate is now supporting [Django Channels](https://channels.readthedocs.io/en/stable/index.html).
- Read more about this [here](https://channels.readthedocs.io/en/stable/index.html)
- The template has a specific structure in terms of organisation, meaning, inside the {{ project_name }} there is a module called `apps` where it contains all the django custom apps in the settings. That setting is in the main {{ project_settings }} and it can be changed or removed.
- You should create a virtual environment in Python 3.6 or higher. This isolates your project and it doesn't break your system

## Installing from the template base

- `django-admin startproject --template=https://github.com/tiagoarasilva/django2-boilerplate/archive/master.zip --extension=py,md,html,txt,scss,sass project_name`
- Make sure you change the "project_name" to the name you desire for you project.
- The tests for the views won't work until you implement the solution to make the tests passing, that means, once you implement the views!

## Docker

- Change the {{ project_name }} in your docker file to the desired name gave to the project when running the previous command.

## {{ project_name }} Docker

-  Run `docker volume create --name={{ project_name }}_db_data`
-  Run `docker-compose up`. It will download all the resources needed to build your docker containers
-  Run `docker-compose exec {{ project_name }} bash` to go inside the container
-  Run `make run` to start the server (inside docker container)
-  Run `make shell` to start the shell_plus

If you desire, you can create somes aliases in your local machine, inside the bash_profile/bashrc/profile to do automatically some previous instructions for you

E.g.:

```shell
alias run_server='docker-compose exec {{ project_name }} bash && make run'
alias shell_plus='docker-compose exec {{ project_name }} bash && make shell'
```

## First run with the project

- Inside docker container:
    - Run `make migrate`. This is a special command inside the Makefile to run the first migration or if you are on windows or you don't want to run the Makefile, just run `python {{ project_name }}/manage.py migrate`
    - Run `python {{ project_name }}/manage.py createsuperuser` to create a super user for yourself
    - It will create a "User Admin" by default as first and last name respectively. This can be changed in `accounts/management/commands/createsuperuser.py`


## Run Tests (If you ran migrations before and need to reconstruct the DB schema)

`make unittests TESTONLY='profiles.tests.models_tests'`
- OR
`make unittests TESTONLY='profiles.tests.models_tests:ProfileUserTest.test_create_user'` for a specific test

## If you only need to run the tests and the models weren't changed before

`make reusedb_unittests TESTONLY='profiles.tests.models_tests`

### Apps

All of your Django "apps" go in this {{ project_name}}/apps directory. These have models, views, forms, urls, 
templates or all of the above. These should be Python packages you would add to
your project's `INSTALLED_APPS` list.


### Requirements for MacOS and Windows

Install Homebrew (MacOS Users)
`/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`

Install OpenSSL or Upgrade (MacOS Users)
`brew install openssl`

### Requirements for Linux (Ubuntu <= 16.10)
Install OpenSSL or Upgrade
`sudo apt-get update`
`sudo apt-get install openssl-server`

Install VirtualenvWrapper
`https://virtualenvwrapper.readthedocs.io/en/latest/install.html`

Upgrade pip
`pip install --upgrade pip`

### Templates

Project-wide templates are located in templates/

### Celery
This projects integrates Redis with RabbitMQ and Celery
