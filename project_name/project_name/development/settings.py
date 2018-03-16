from {{ project_name }}.settings import *

# To see outgoing email dumped to a terminal, uncomment the following and
# run "python -m smtpd -n -c DebuggingServer localhost:1025"
DEBUG = True

DJANGOENV = 'development'

try:
    import readline
    readline  # make pyflakes happy, readline makes interactive mode keep history
except ImportError:
    # no readline on Windows
    pass

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

INSTALLED_APPS += [
    'django_nose',
    'django_extensions',
    'debug_toolbar',
    'template_repl',
]

DJANGO_DEBUG_TOOLBAR = True
SHOW_TOOLBAR_CALLBACK = True

COMPRESS_ENABLED = False
COMPRESS_OFFLINE = True

BROKER_URL = 'amqp://rabbit_user:rabbit_user_default_pass@localhost:5672/'
