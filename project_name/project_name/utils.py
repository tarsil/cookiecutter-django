# mostly resolution via AWS, separated to here to make testing easier


def make_memcached_cache(memcached_locations):
    return {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': memcached_locations,
        },
        'api': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': memcached_locations,
            'TIMEOUT': 86400 * 365,
            'KEY_PREFIX': 'api2',  # 2 => includes slugs for objects
        },
        'staticfiles': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': memcached_locations,
            'TIMEOUT': 86400 * 365,
            'KEY_PREFIX': 'staticfiles',
        },
        'depictions': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': memcached_locations,
            'TIMEOUT': 86400 * 365,
            'KEY_PREFIX': 'depictions',
        },
        'thumbnails': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': memcached_locations,
            'TIMEOUT': 86400 * 365,
            'KEY_PREFIX': 'thumbnails',
        },
        'sessions': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': memcached_locations,
        },
    }
