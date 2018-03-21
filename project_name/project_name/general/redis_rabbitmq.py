'''
The setup for rabbitmq message broker (we can also user Redis for this)
'''
import os
import djcelery
from kombu import Exchange, Queue, serialization
from {{ project_name }}.utils import make_memcached_cache


# BROKER_HOST = '127.0.0.1'
BROKER_PORT = 5672
BROKER_VHOST = '/'
BROKER_USER = '{{ project_name }}'
BROKER_PASSWORD = '!!bro!!k!er'
BROKER_TRANSPORT_OPTIONS = {'confirm_publish': True}
CELERY_CREATE_MISSING_QUEUES = True
CELERY_RESULT_PERSISTENT = True

# REDIS

SESSION_CACHE_ALIAS = "sessions"
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

MEMCACHED_ENDPOINTS = [
    '127.0.0.1:11211',
]
CACHES = make_memcached_cache(MEMCACHED_ENDPOINTS)
CACHES["default"] = {
    'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
}
CACHES['sessions'] = {
    'BACKEND': 'redis_cache.RedisCache',
    'LOCATION': 'redis:6379',
    'OPTIONS': {
        'DB': 10,
    }
}

REDIS_HOSTNAME = 'localhost'
REDIS_PORT = 6379
REDIS_SERVER = (REDIS_HOSTNAME, REDIS_PORT, 0)  # host, port, db
REDIS_PASSWORD = ''
REDIS_DB = 1  # keep cache entries in a different db so we can clear them easily
REDIS_HOST = os.environ.get('REDIS_PORT_6379_TCP_ADDR', 'redis')


# RABBITMQ
# CELERY_BROKER_HOST = '127.0.0.1'
CELERY_BROKER_USER = 'rabbit_user'
CELERY_BROKER_PASSWORD = 'rabbit_user_default_pass'
RABBIT_HOSTNAME = os.environ.get('RABBIT_PORT_5672_TCP', 'rabbit')

if RABBIT_HOSTNAME.startswith('tcp://'):
    RABBIT_HOSTNAME = RABBIT_HOSTNAME.split('//')[1]

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', '')
if not CELERY_BROKER_URL:
    CELERY_BROKER_URL = 'amqp://{user}:{password}@{hostname}/{vhost}/'.format(
        user=os.environ.get('RABBIT_ENV_USER', CELERY_BROKER_USER),
        password=os.environ.get('RABBIT_ENV_RABBITMQ_PASS', CELERY_BROKER_PASSWORD),
        hostname=RABBIT_HOSTNAME,
        vhost=os.environ.get('RABBIT_ENV_VHOST', ''))

# We don't want to have dead connections stored on rabbitmq, so we have to negotiate using heartbeats
CELERY_BROKER_HEARTBEAT = "30"
# if not CELERY_BROKER_URL.endswith(CELERY_BROKER_HEARTBEAT):
#     CELERY_BROKER_URL += CELERY_BROKER_HEARTBEAT

CELERY_BROKER_POOL_LIMIT = 1
CELERY_BROKER_CONNECTION_TIMEOUT = 10


# CELERY CONFIGURATION
# CONFIGURE QUEUES, CURRENTLY WE HAVE ONLY ONE
CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = (
    Queue('queue', Exchange('queue'), routing_key='queue'),
)


# SENSIBLE SETTINGS FOR CELERY
CELERY_ALWAYS_EAGER = False
CELERY_ACKS_LATE = True
CELERY_TASK_PUBLISH_RETRY = True
CELERY_DISABLE_RATE_LIMITS = False

# BY DEFAULT WE WILL IGNORE RESULT
# IF YOU WANT TO SEE RESULTS AND TRY OUT TASKS INTERACTIVELY, CHANGE IT TO FALSE
# OR CHANGE THIS SETTING ON TASKS LEVEL
CELERY_IGNORE_RESULT = True
CELERY_SEND_TASK_ERROR_EMAILS = False
CELERY_TASK_RESULT_EXPIRES = 600

# SET REDIS AS CELERY RESULT BACKEND
CELERY_RESULT_BACKEND = 'redis://%s:%d/%d' % (REDIS_HOSTNAME, REDIS_PORT, REDIS_DB)
CELERY_REDIS_MAX_CONNECTIONS = 1

# DON'T USE PICKLE AS SERIALIZER, JSON IS MUCH SAFER
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYD_HIJACK_ROOT_LOGGER = False
CELERYD_PREFETCH_MULTIPLIER = 1
CELERYD_MAX_TASKS_PER_CHILD = 1000

# UTC
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True

# ACTIVATE SETTINGS
djcelery.setup_loader()
