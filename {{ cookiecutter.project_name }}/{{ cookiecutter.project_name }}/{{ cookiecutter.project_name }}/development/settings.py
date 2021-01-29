# type: ignore
from ..settings import *

# To see outgoing email dumped to a terminal, uncomment the following and
# run "python -m smtpd -n -c DebuggingServer localhost:1025"
DEBUG = True

DJANGOENV = os.environ.get("DJANGOENV", "development")

INSTALLED_APPS += [
    'django_nose',
    'debug_toolbar',
    'template_repl',
    'django_extensions',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

# FOR THE DEBUG TOOLBAR
INTERNAL_IPS = [
    "127.0.0.1",
    "172.16.0.0/16",
]

STATICFILES_DIRS += [STATICI18N_ROOT]

DJANGO_DEBUG_TOOLBAR = False

def show_toolbar(request):
        return True

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
}

SHOW_TOOLBAR_CALLBACK = True

# STATICS RUNNING LOCALLY
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

STATIC_URL = '/static/'

MEDIA_ROOT = '/{{ cookiecutter.project_name }}-media'
MEDIA_URL = '/media/'

BROKER_URL = 'amqp://rabbit_user:rabbit_user_default_pass@localhost:5672/'

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 8640000
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
X_FRAME_OPTIONS = 'DENY'
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "http")
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

SHELL_PLUS_MODEL_IMPORTS_RESOLVER = 'django_extensions.collision_resolvers.FullPathCR'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    "handlers": {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "ERROR",
        },
        "{{ cookiecutter.project_name }}.apps": {
            "handlers": [],
            "propagate": False,
        },
    }
}

try:
    from .local_settings import *
except ImportError:
    pass
