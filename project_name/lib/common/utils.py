import functools

import django.core.urlresolvers
from django.conf import settings


"""\
A wrapper for reverse that always sets the URLConf to the {{ project_name }}.
This is safe to use from the API, unlike the normal reverse().
"""
reverse = functools.partial(
    django.core.urlresolvers.reverse, urlconf=settings.ROOT_URLCONF)
