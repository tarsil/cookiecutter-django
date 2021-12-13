"""
Add the settings to be overriden in the live system

REST_FRAMEWORK.update({'COMPACT_JSON': True})
"""
import ast
from base64 import b64decode

from ..settings import *  # noqa: F403,F401
from .databases import *  # noqa: F403,F401

SECRET_KEY = os.environ['SECRET_KEY']
DJANGOENV = os.environ.get("DJANGOENV", "staging")


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(SITE_ROOT, 'templates'),
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.csrf',
                'lib.context_processor.export_env_vars',

            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 8640000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

CORS_ALLOWED_ORIGINS = ast.literal_eval(os.environ.get('CORS_ALLOWED_ORIGINS', '[]'))
ALLOWED_HOSTS = ast.literal_eval(os.environ.get('ALLOWED_HOSTS', '[]'))

REST_FRAMEWORK.update({'COMPACT_JSON': True})
