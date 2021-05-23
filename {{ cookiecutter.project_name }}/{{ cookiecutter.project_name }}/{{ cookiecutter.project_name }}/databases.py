import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'pgbouncer',
        'USER': 'default',
        'PASSWORD': 'bouncer',
        'NAME': 'postgres',
        'PORT': 6432
    }
}
