'''
The setup for rabbitmq message broker (we can also user Redis for this)
'''
import os
from kombu import Exchange, Queue

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379',
        'KEY_PREFIX': 'cache',
        'OPTIONS': {
            'SERIALIZER': 'django_redis.serializers.json.JSONSerializer',
        },
    },
}

CELERY_BROKER_URL = os.environ['BROKER_URL']

CELERY_BROKER_HEARTBEAT = 30
CELERY_BROKER_HEARTBEAT_CHECKRATE = 3
CELERY_BROKER_POOL_LIMIT = 10
CELERY_BROKER_CONNECTION_TIMEOUT = 3
CELERY_BROKER_CONNECTION_MAX_RETRIES = 0


# CELERY CONFIGURATION
# CONFIGURE QUEUES, CURRENTLY WE HAVE ONLY ONE
CELERY_RESULT_PERSISTENT = True

CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_DEFAULT_ROUTING_KEY = 'default'

CELERY_TASK_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('linezap', Exchange('linezap'), routing_key='default'),
)

# IMPORT ROUTES AND CRONTAB
from {{ cookiecutter.project_name }}.general.celery_routes_crontab import *


# SENSIBLE SETTINGS FOR CELERY
CELERY_TASK_PUBLISH_RETRY = True

# BY DEFAULT WE WILL IGNORE RESULT
# IF YOU WANT TO SEE RESULTS AND TRY OUT TASKS INTERACTIVELY, CHANGE IT TO FALSE
# OR CHANGE THIS SETTING ON TASKS LEVEL
CELERY_TASK_IGNORE_RESULT = True
CELERY_RESULT_EXPIRES = 600

# SET CELERY RESULT BACKEND
CELERY_RESULT_BACKEND = 'disabled://'

CELERY_WORKER_HIJACK_ROOT_LOGGER = False
CELERY_WORKER_PREFETCH_MULTIPLIER = 8
CELERY_WORKER_MAX_TASKS_PER_CHILD = 10000
CELERY_RESULT_COMPRESSION = 'bzip2'
CELERY_TASK_COMPRESSION = 'bzip2'
CELERY_TASK_TIME_LIMIT = 3 * 60 * 60  # 3 hours
CELERY_TASK_SOFT_TIME_LIMIT = CELERY_TASK_TIME_LIMIT - 5 * 60  # 5 minutes before the hard timeout
