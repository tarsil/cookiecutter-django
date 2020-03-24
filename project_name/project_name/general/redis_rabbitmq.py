'''
The setup for rabbitmq message broker (we can also user Redis for this)
'''
import os
from kombu import Exchange, Queue, serialization
import djcelery

# REDIS

SESSION_CACHE = "sessions"
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

REDIS_HOSTNAME = 'localhost'
REDIS_PORT = 6379
REDIS_SERVER = (REDIS_HOSTNAME, REDIS_PORT, 0)  # host, port, db
REDIS_PASSWORD = ''
REDIS_DB = 1  # keep cache entries in a different db so we can clear them easily
REDIS_HOST = os.environ.get('REDIS_PORT_6379_TCP_ADDR', 'redis')


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



# RABBITMQ
RABBIT_HOSTNAME = os.environ.get('RABBIT_PORT_5672_TCP', 'rabbit')

if RABBIT_HOSTNAME.startswith('tcp://'):
    RABBIT_HOSTNAME = RABBIT_HOSTNAME.split('//')[1]

BROKER_URL = os.environ.get('BROKER_URL', '')
if not BROKER_URL:
    BROKER_URL = 'amqp://{user}:{password}@{hostname}/{vhost}/'.format(
        user=os.environ.get('RABBIT_ENV_USER', 'rabbit_user'),
        password=os.environ.get('RABBIT_ENV_RABBITMQ_PASS', 'rabbit_user_default_pass'),
        hostname=RABBIT_HOSTNAME,
        vhost=os.environ.get('RABBIT_ENV_VHOST', ''))


# We don't want to have dead connections stored on rabbitmq, so we have to negotiate using heartbeats
BROKER_HEARTBEAT = '30'
if not BROKER_URL.endswith(BROKER_HEARTBEAT):
    BROKER_URL += BROKER_HEARTBEAT

BROKER_POOL_LIMIT = 1
BROKER_CONNECTION_TIMEOUT = 10


# CELERY CONFIGURATION
# CONFIGURE QUEUES, CURRENTLY WE HAVE ONLY ONE
CELERY_RESULT_PERSISTENT = True

CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_DEFAULT_ROUTING_KEY = 'default'

CELERY_TASK_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('linezap', Exchange('default'), routing_key='default'),
)

# IMPORT ROUTES AND CRONTAB
from linezap.general.celery_routes_crontab import *


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

# ACTIVATE SETTINGS
djcelery.setup_loader()
