DEFAULT_GOAL := help

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: clean_pyc

.PHONY: clean_pyc
clean_pyc: ## Clean all *.pyc in the system
	find . -type f -name "*.pyc" -delete || true

.PHONY: migrate
migrate: # Runs the migrations
	python {{ cookiecutter.project_name }}/manage.py migrate --noinput

.PHONY: migrations
migrations: ## Generate migrations
	python {{ cookiecutter.project_name }}/manage.py makemigrations

.PHONY: requirements
requirements: ## Install the production requirements
	pip3 install -r requirements/common.txt

.PHONY: requirements-dev
requirements-dev: ## Install the production requirements
	pip3 install -r requirements/development.txt

.PHONY: requirements-deployment
requirements-deployment: ## Install the production requirements
	pip3 install -r requirements/deployment.txt

.PHONY: test
test: ## Runs the unit tests from the scratch by recreating the testing database
	cd {{ cookiecutter.project_name }} 										&&\
	pytest $(TESTONLY) --disable-pytest-warnings -s -vv $(DB)				&&\
	cd .

.PHONY: mypy
mypy: ## Runs MyPy type checking
	mypy {{ cookiecutter.project_name }}/

.PHONY: run
run: ## Starts the dev server
	DJANGO_SETTINGS_MODULE={{ cookiecutter.project_name }}.development.settings python {{ cookiecutter.project_name }}/manage.py runserver_plus 0.0.0.0:8000

.PHONY: asgi
asgi: ## Starts the local server in ASGI mode
	DJANGO_SETTINGS_MODULE={{ cookiecutter.project_name }}.development.settings python {{ cookiecutter.project_name }}/manage.py runserver 0.0.0.0:8000

.PHONY: shell
shell:
	DJANGO_SETTINGS_MODULE={{ cookiecutter.project_name }}.development.settings python {{ cookiecutter.project_name }}/manage.py shell_plus

.PHONY: dramatiq
dramatiq: ## Starts DramatiQ task manager
	cd {{ cookiecutter.project_name }} &&\
	DJANGO_SETTINGS_MODULE={{ cookiecutter.project_name }}.development.settings python manage.py rundramatiq

.PHONY: show_urls
show_urls:
	DJANGO_SETTINGS_MODULE={{ cookiecutter.project_name }}.development.settings python {{ cookiecutter.project_name }}/manage.py show_urls

.PHONY: validate_templates
validate_templates:
	DJANGO_SETTINGS_MODULE={{ cookiecutter.project_name }}.development.settings python {{ cookiecutter.project_name }}/manage.py validate_templates

.PHONY: createsuperuser
createsuperuser: ## Creates a super user in the database
	DJANGO_SETTINGS_MODULE={{ cookiecutter.project_name }}.development.settings python {{ cookiecutter.project_name }}/manage.py createsuperuser

.PHONY: start_docker
start_docker: ## Starts the dev environment
	docker-compose up -d

.PHONY: start_docker_logs
start_docker_logs: ## Starts the dev environment
	docker-compose up

.PHONY: scheduler
scheduler: ## Starts the schedule
	python {{ cookiecutter.project_name }}/manage.py scheduler

ifndef VERBOSE
.SILENT:
endif
