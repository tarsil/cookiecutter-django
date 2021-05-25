import os

{%- if cookiecutter.without_mongo == "N" %}
import mongoengine
{%-endif %}


DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ.get('{{ cookiecutter.project_name }}_PGBOUNCER_HOST', 'pgbouncer'),
        'USER': 'default',
        'PASSWORD': 'bouncer',
        'NAME': os.environ.get('{{ cookiecutter.project_name }}_PGBOUCER_NAME'),
        'PORT': 6432,
        'OPTIONS': {
            'connect_timeout': 5,  # seconds
        }
    },
}

{% if cookiecutter.without_mongo == "N" -%}
MONGO_USER = os.environ.get('{{ cookiecutter.project_name }}_MONGODB_USER_HOST', 'root'),
MONGO_PASS = os.environ.get('{{ cookiecutter.project_name }}_MONGODB_PASSWORD', 'mongoadmin'),
MONGO_HOST = os.environ.get('{{ cookiecutter.project_name }}_MONGODB_HOST', 'mongodb')
MONGO_DB_NAME = os.environ.get('{{ cookiecutter.project_name }}_MONGODB_DB_NAME', 'mongodb')
MONGO_DATABASE_HOST = f"mongodb://%s:%s@%s/%s" % (MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_DB_NAME)

mongoengine.connect(MONGO_DB_NAME, host=MONGO_DATABASE_HOST)
{% endif %}
