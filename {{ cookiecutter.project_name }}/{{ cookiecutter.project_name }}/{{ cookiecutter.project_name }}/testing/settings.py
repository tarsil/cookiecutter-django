# type: ignore
"""
testing.settings will pull in (probably global) local_settings,
This is a special thanks to David Dyball for helping me understand and build something very familiar to me
in terms of settings and how to set them up

To all who contribute for this, thank you very much.

If you are using windows by default, the permissions to access subfolders for tests are disabled
Activate them using NOSE_INCLUDE_EXE = 1 or an environment variable in your OS with the same name and value
"""
from ..settings import *
from .databases import *
import os

SECRET_KEY = os.environ.get("SECRET_KEY", "x7@y+)ixs_gdewzjw!br7ee#e4ovat7xd3%5&m8i6ws(d=5p#x")

#
# Other settings
#
DEBUG = True
TESTING = True

#
# Tells the django environment
#
DJANGOENV = os.environ.get("DJANGOENV", "testing")

REUSE_DB = bool(int(os.environ.get("REUSE_DB", 0)))

if REUSE_DB:
    DATABASE_ROUTERS = []

POSTGIS_TEMPLATE = "template_postgis"
POSTGIS_VERSION = (2, 1, 2)

# If you have Django Debug Toolbar installed
DEBUG_TOOLBAR_PANELS = ()

# Disable the Secure SSL Redirect (special thanks to @DD)
SECURE_SSL_REDIRECT = False

# Use this if you have local_settings.pt file
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
MEDIA_URL = "/media/"
STATIC_ROOT = "/tmp/assets-upload"
STATIC_URL = "/static/"
MEDIA_ROOT = "/tmp/media-root"

# Give ourselves a test instance of redis (another special thanks to @DD for this)
REDIS_SERVER = ("redis", 6379, 2)  # host, port, dbs
REDIS_PASSWORD = None

# We don't want to run Memcached for tests.
SESSION_ENGINE = "django.contrib.sessions.backends.db"

CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"},
    "staticfiles": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"},
}

# We don't care about secure password for tests, use MD5 which is faster.
PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher", "django.contrib.auth.hashers.SHA1PasswordHasher")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "root": {"level": "INFO", "handlers": ["console"]},
    "formatters": {"verbose": {"format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"}},
    "handlers": {"console": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "verbose"}},
}

MIDDLEWARE = list(MIDDLEWARE)

# DRAMATIQ TESTING - https://github.com/Bogdanp/django_dramatiq
DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.stub.StubBroker",
    "OPTIONS": {},
    "MIDDLEWARE": [
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Pipelines",
        "dramatiq.middleware.Retries",
        "django_dramatiq.middleware.AdminMiddleware",
        "django_dramatiq.middleware.DbConnectionsMiddleware",
    ],
}
