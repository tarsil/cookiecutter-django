import {{ project_name }}.utils

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
