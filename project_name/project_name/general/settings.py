from django.utils.translation import ugettext_lazy

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

CANONICAL_SITE_URL = 'www.{{ project_name }}.com'

AUTH_PROFILE_MODULE = 'profiles.profile'
ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: '/user/%i/' % u.profile.pk,
}

# Sessions
POSTGRES_HOSTNAME = 'localhost'

# LANGUAGES
LANGUAGE_CODE = 'en-gb'

LANGUAGES = (
    ('en-us', ugettext_lazy('American English')),
    ('en-gb', ugettext_lazy('British English')),
)

# Pseudolanguage is used for Enabling Crowdin translation mode
PSEUDO_LANGUAGE = 'zu'
VISIBLE_LANGUAGES = tuple(x for x in LANGUAGES if x[0] != PSEUDO_LANGUAGE)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    "handlers": {
        'bugsnag': {
            'level': 'ERROR',
            'class': 'bugsnag.handlers.BugsnagHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
        'investigation': {
            "level": "INFO",
            "class": "bugsnag.handlers.BugsnagHandler"
        }
    },
    "loggers": {
        "django.request": {
            "level": "ERROR",
            "propagate": True,
        },
        "celery": {
            "handlers": ["console", "bugsnag"],
            "level": "INFO",
            "propagate": True
        },
        "httpstream": {
            "handlers": ["console", "bugsnag"],
            "level": "ERROR",
            "propagate": True
        },
        "elasticsearch": {
            "handlers": ["console", "bugsnag"],
            "level": "WARNING",
            "propagate": False
        },
        "urllib3": {
            "handlers": ["console", "bugsnag"],
            "level": "WARNING",
            "propagate": False
        },
        "celery.investigation": {
            "level": "INFO",
            "handlers": ["investigation"],
            "propagate": False
        }

    }
}

