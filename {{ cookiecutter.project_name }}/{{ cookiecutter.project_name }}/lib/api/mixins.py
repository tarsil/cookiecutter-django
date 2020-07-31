# pragma: no cover
"""
All the mixins that can be used in the system and for Django REST Framework Views
"""
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class AnonymousAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        return (request._request.user, None)


class AuthMeta(type):
    """Metaclass to create/read from permissions property
    """
    def __new__(cls, name, bases, attrs):
        permissions = []
        for base in bases:
            if hasattr(base, 'permissions'):
                permissions.extend(base.permissions)
        attrs['permissions'] = permissions + attrs.get('permissions', [])
        return type.__new__(cls, name, bases, attrs)


class AccessMixin(metaclass=AuthMeta):
    """
    Django rest framework doesn't append permission_classes on inherited models which can cause issues when
    it comes to call an API programmatically, this way we create a metaclass that will read from a property custom
    from our subclasses and will append to the default `permission_classes` on the subclasses of AccessMixin
    """
    pass


class BaseAuthView(AccessMixin, APIView):
    """
    Base APIView requiring login credentials to access it from the inside of the platform
    Or via request (if known)
    """
    permissions = [IsAuthenticated]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.permission_classes = self.permissions
