import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BD_NON_DEFAULT = u'db_non_default'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    # BD_NON_DEFAULT: {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'postgres',
    #     'USER': 'postgres',
    #     'PASSWORD': 'postgres',
    #     'HOST': 'postgres',
    #     'PORT': '5432',
    # }
}
