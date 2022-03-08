import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'USER': 'default',
        'PASSWORD': 'bouncer',
        'NAME': 'postgres',
        'PORT': 6432
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
            'host': 'localhost',
            'port': 27017,
            'username': 'root',
            'password': "mongoadmin",
            'authSource': 'admin',
            'authMechanism': 'SCRAM-SHA-1'
        }
    }
    {%-endif %}
}
