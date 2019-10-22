import os

from django.conf import settings
from django import template
from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.http import urlquote

register = template.Library()


@register.simple_tag
def media(path):
    "Template tag which inserts the relevant prefix for the media files"
    return u"%s%s" % (settings.MEDIA_URL, urlquote(path))


@register.simple_tag
def minified_static(path):
    """
    A template tag that returns the minified URL to a file
    using staticfiles' storage backend. If we are in debugging
    mode, this will return the non-minified version.
    """

    if settings.DEBUG:
        return staticfiles_storage.url(path)
    split_path = os.path.splitext(path)
    new_path = "%s.min%s" % (split_path[0], split_path[1])
    return staticfiles_storage.url(new_path)
