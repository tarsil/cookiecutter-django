"""
The setup for rabbitmq message broker (we can also user Redis for this)
"""

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
