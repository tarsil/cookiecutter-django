import functools

from django.urls import reverse
from django.conf import settings


"""
A wrapper for reverse that always sets the URLConf to the {{ cookiecutter.project_name }}.
This is safe to use from the API, unlike the normal reverse().
"""
reverse = functools.partial(
    reverse, urlconf=settings.ROOT_URLCONF)
