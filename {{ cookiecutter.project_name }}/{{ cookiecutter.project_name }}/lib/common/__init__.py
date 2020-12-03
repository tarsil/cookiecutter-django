import functools
import django.urls
from django.conf import settings

reverse = functools.partial(django.urls.reverse, urlconf="myproject.urls")


def only_run_on_live(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if settings.DJANGOENV == "live":
            return func(*args, **kwargs)
    return wrapper
