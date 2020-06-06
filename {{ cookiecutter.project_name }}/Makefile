clean: clean_pyc
clean_pyc:
	find . -type f -name "*.pyc" -delete || true

migrate:
	python $(PROJECT_NAME)/manage.py migrate --noinput

migrations:
	python $(PROJECT_NAME)/manage.py makemigrations

reusedb_unittests:
	cd $(PROJECT_NAME) &&\
	DJANGO_SETTINGS_MODULE=$(PROJECT_NAME).testing.settings REUSE_DB=1 DJANGOENV=testing python manage.py test $(TESTONLY)  --exe --with-specplugin  --keepdb &&\
	cd ..

unittests:
	cd $(PROJECT_NAME) &&\
	DJANGO_SETTINGS_MODULE=$(PROJECT_NAME).testing.settings DJANGOENV=testing python manage.py test $(TESTONLY) --exe --with-specplugin
	cd ..
run:
	python $(PROJECT_NAME)/manage.py runserver_plus 0.0.0.0:8000 --settings=$(PROJECT_NAME).$(ENVIRONMENT).settings

shell:
	python $(PROJECT_NAME)/manage.py shell_plus --settings=$(PROJECT_NAME).$(ENVIRONMENT).settings

celery_django:
	python $(PROJECT_NAME)/manage.py celery -A $(PROJECT_NAME) worker --logleve=INFO --settings=$(PROJECT_NAME).$(ENVIRONMENT).settings

celery:
	python $(PROJECT_NAME)/manage.py celery worker -A $(PROJECT_NAME).celery --logleve=INFO --settings=$(PROJECT_NAME).$(ENVIRONMENT).settings

show_urls:
	python $(PROJECT_NAME)/manage.py show_urls --settings=$(PROJECT_NAME).$(ENVIRONMENT).settings

validate_templates:
	python $(PROJECT_NAME)/manage.py validate_templates --settings=$(PROJECT_NAME).$(ENVIRONMENT).settings
