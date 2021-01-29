# pragma: no cover
"""
All the mixins that can be used in the system and for Django REST Framework Views
"""
from rest_framework import authentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class AnonymousAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        return (request._request.user, None)


class AuthMeta(type):
    """Metaclass to create/read from permissions property"""
    def __new__(cls, name, bases, attrs):
        permissions = []
        for base in bases:
            if hasattr(base, 'permissions'):
                permissions.extend(base.permissions)
        attrs['permissions'] = permissions + attrs.get('permissions', [])
        return type.__new__(cls, name, bases, attrs)


class AccessMixin(metaclass=AuthMeta):
    """Django rest framework doesn't append permission_classes on inherited models which can cause issues when
    it comes to call an API programmatically, this way we create a metaclass that will read from a property custom
    from our subclasses and will append to the default `permission_classes` on the subclasses of AccessMixin
    """
    pass


class AuthMixin(AccessMixin, APIView):
    """Base APIView requiring login credentials to access it from the inside of the platform
    Or via request (if known)
    """
    permissions = [IsAuthenticated]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.permission_classes = self.permissions

    def get_host_url(self):
        """Returns the host url (localhost, staging, preview, live)"""
        return self.request.get_host()


class NoPermissionsMixin(APIView):
    """Remove all the permissions from a view"""
    permission_classes = []


class RequiredUserContextView(GenericAPIView):
    """Handles with Generics for user specific views"""

    def get_serializer(self, *args, **kwargs):
        """
        Args:
          *args:
          **kwargs:
        Returns:
          deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        """ """
        context = super().get_serializer_context()
        context.update({
            'request': self.request,
            'user': self.request.user,
        })
        return context
