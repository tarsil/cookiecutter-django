{{ cookiecutter.project_name }}
===============================================================================

## Initial notes

* The template is using foundation as a framework but this can be changed by your personal preference, you only need to update the references in the `static` and `templates` folder.
* Inside the views located in accounts, there are some that you need to create your own files, such as the registration or change password, the code is there, you only need to place the HTML inside the proper directory. The only HTML placed and working is the login and the homepage to allow you to do a first run.
* Comes with a bunch of plugins for many kinds of projects. Not all of them are needed, feel free to remove what you don't need
* This template is now supporting [Django Channels](https://channels.readthedocs.io/en/stable/index.html).
* The template has a specific structure in terms of organisation, meaning, inside the {{ cookiecutter.project_name }} there is a module called `apps` where it contains all the django custom apps in the settings. 
That setting is in the main project settings and it can be changed or removed.
* You should create a virtual environment in Python 3.6 or higher. This isolates your project and it doesn't break your system

## Using the template

* `cookiecutter https://github.com/tiagoarasilva/cookicutter-django` and follow the instructions.
    **When giving a name to your project, avoid dashes by using underscores instead.**
* The tests for the views won't work until you implement the solution to make the tests passing, that means, once you implement the views!


## {{ cookiecutter.project_name }} Docker

*  Run `docker volume create --name={{ cookiecutter.project_name }}_db_data`
*  Run `docker-compose up`. It will download all the resources needed to build your docker containers
*  Run `docker-compose exec {{ cookiecutter.project_name }} bash` to go inside the container
*  Run `make run` to start the server (inside docker container)
*  Run `make shell` to start the shell_plus

If you desire, you can create some aliases in your local machine, inside the `bash_profile or bashrc orprofile` to do automatically 
some of the previous instructions for you.

E.g.:

```shell
alias run_server='docker-compose exec {{ cookiecutter.project_name }} bash && make run'
alias shell_plus='docker-compose exec {{ cookiecutter.project_name }} bash && make shell'
```

## First run with the project

* Inside docker container:
    * Run `make migrate`. This is a special command inside the Makefile to run the first migration or just run `python {{ cookiecutter.project_name }}/manage.py migrate`
    * Run `python {{ cookiecutter.project_name }}/manage.py createsuperuser` to create a super-user for yourself
    * It will create a "User Admin" by default as first and last name, respectively. This can be changed in `accounts/management/commands/createsuperuser.py`

## Requirements

```shell
pip install -r requirements/development.txt
```

## Run Tests (If you ran migrations before and need to reconstruct the DB schema)

`make unittests`

## If you only need to run the tests and the models weren't changed before

`make reusedb_unittests TESTONLY='_name_of_django_app_.tests.py`

### Extra

Install VirtualenvWrapper
`https://virtualenvwrapper.readthedocs.io/en/latest/install.html`
