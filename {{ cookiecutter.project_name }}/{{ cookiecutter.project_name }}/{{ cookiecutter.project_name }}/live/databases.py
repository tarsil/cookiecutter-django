import os

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
    {%-if cookiecutter.without_mongo == "N" %}
    'mongodb': {
        'ENGINE': 'djongo',
        'ENFORCE_SCHEMA': True,
        'LOGGING': {
            'version': 1,
            'loggers': {
                'djongo': {
                    'level': 'DEBUG',
                    'propogate': False,
                }
            },
         },
        'NAME': 'mongodb',
        'CLIENT': {
            'host': os.environ.get('WHALAP_MONGODB_HOST', 'mongodb'),
            'port': os.environ.get('WHALAP_MONGODB_PORT', 'mongodb'),
            'username': os.environ.get('WHALAP_MONGODB_USER_HOST', 'root'),
            'password': os.environ.get('WHALAP_MONGODB_PASSWORD', 'mongoadmin'),
            'authSource': 'admin',
            'authMechanism': 'SCRAM-SHA-1'
        }
    }
    {%-endif %}
}
