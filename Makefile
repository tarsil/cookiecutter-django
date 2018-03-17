clean: clean_pyc
clean_pyc:
	find . -type f -name "*.pyc" -delete || true

migrate:
	python3 $(PROJECT_NAME)/manage.py migrate --noinput

migrations:
	python3 $(PROJECT_NAME)/manage.py makemigrations

reusedb_unittests:
	DJANGO_SETTINGS_MODULE=$(PROJECT_NAME).testing.settings REUSE_DB=1 DJANGOENV=testing python3 $(PROJECT_NAME)/manage.py test $(TESTONLY) --with-specplugin  --keepdb

unittests:
	DJANGO_SETTINGS_MODULE=$(PROJECT_NAME).testing.settings DJANGOENV=testing python3 $(PROJECT_NAME)/manage.py test $(TESTONLY) --with-specplugin

run:
	python3 $(PROJECT_NAME)/manage.py runserver_plus 0.0.0.0:8000 --settings=$(PROJECT_NAME).$(ENVIRONMENT).settings

shell:
	python3 $(PROJECT_NAME)/manage.py shell_plus --settings=$(PROJECT_NAME).$(ENVIRONMENT).settings

celery:
	python3 saturn/manage.py celery worker -A celery --logleve=INFO --settings=$(PROJECT_NAME).$(ENVIRONMENT).settings

show_urls:
	python3 $(PROJECT_NAME)/manage.py show_urls --settings=$(PROJECT_NAME).$(ENVIRONMENT).settings

validate_templates:
	python3 $(PROJECT_NAME)/manage.py validate_templates --settings=$(PROJECT_NAME).$(ENVIRONMENT).settings
