from django.template import Library
from django.contrib.staticfiles.storage import staticfiles_storage

register = Library()


@register.assignment_tag(name='get_static_path')
def static_path(path):
    return staticfiles_storage.url(path)
