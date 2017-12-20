from django.template import Library
from accounts.models import ProfileType

register = Library()


@register.simple_tag
def profiles(user):
    profile_type = ProfileType.objects.filter( profile=user.profile)
    return profile_type
