import os

from {{ project_name }}.databases import *
from {{ project_name }}.general.settings import *
from {{ project_name }}.third_parties.blacklist_domains import *
from {{ project_name }}.general.redis_rabbitmq import *

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
{{ project_name }}_VERSION = os.path.basename(os.path.dirname(SITE_ROOT))
DJANGOENV = None

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(SITE_ROOT, 'apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# IMPORTANT!:
# You must keep this secret, you can store it in an
# environment variable and set it with:
# export SECRET_KEY="secret-export!key-781"
# https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/#secret-key
SECRET_KEY = "secret_change_this_after"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition
SITE_ID = 1

BASE_INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'django.contrib.redirects',
    'djcelery',
    'lib.common',
    'lib.audit',
    'lib.cache',
    'lib.viewslibrary',
    'statici18n',
    'compressor',
    'rest_framework',
    'channels',
]

INSTALLED_APPS = [
    'accounts',
    'api',
] + BASE_INSTALLED_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',

    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 20
}


ROOT_URLCONF = '{{ project_name }}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(SITE_ROOT, 'templates'),
            os.path.join(SITE_ROOT, 'static'),
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.csrf',

            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'debug': DEBUG,
        },
    },
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = []

STATICFILES_STORAGE = 'lib.storage.CachedStaticFilesStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Statici18n Config
STATICI18N_ROOT = os.path.join(SITE_ROOT, 'static')

STATICFILES_DIRS += [STATICI18N_ROOT]

STATIC_ROOT = os.path.join(SITE_ROOT, 'staticfiles')

LOCALE_PATHS = [os.path.join(SITE_ROOT, 'locale')]

COMPRESS_ROOT = '/tmp/pr-static'
COMPRESS_ENABLED = True

WSGI_APPLICATION = '{{ project_name }}.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'accounts.User'

# Internationalization
# https://docs.djangoproject.com/en/1.11.4/topics/i18n/

LANGUAGE_CODE = 'en-us'

INTERNAL_IPS = ('127.0.0.1', '192.168.56.1', '10.0.2.2',)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Pull slug max_length out ot
SLUG_MAX_LENGTH = 64

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
