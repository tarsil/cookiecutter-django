import {{ project_name }}.utils
from django.utils.translation import ugettext_lazy


SESSION_CACHE_ALIAS = "sessions"
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

CANONICAL_SITE_URL = 'www.ltplabs.com'

AUTH_PROFILE_MODULE = 'profiles.profile'
ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: '/user/%i/' % u.profile.pk,
}


# Sessions
POSTGRES_HOSTNAME = 'localhost'
REDIS_HOSTNAME = 'localhost'

MEMCACHED_ENDPOINTS = [
    '127.0.0.1:11211',
]

CACHES = {{ project_name }}.utils.make_memcached_cache(MEMCACHED_ENDPOINTS)

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

# REDIS
REDIS_SERVER = ('localhost', 6379, 0)  # host, port, db
REDIS_PASSWORD = ""
CACHE_REDIS_DB = 1  # keep cache entries in a different db so we can clear them easily
REDIS_RECOMMENDATIONS_DB = 9


# LANGUAGES
LANGUAGE_CODE = 'en-gb'

LANGUAGES = (
    ('en-us', ugettext_lazy('American English')),
    ('en-gb', ugettext_lazy('British English')),
)

# Pseudolanguage is used for Enabling Crowdin translation mode
PSEUDO_LANGUAGE = 'zu'
VISIBLE_LANGUAGES = tuple(x for x in LANGUAGES if x[0] != PSEUDO_LANGUAGE)