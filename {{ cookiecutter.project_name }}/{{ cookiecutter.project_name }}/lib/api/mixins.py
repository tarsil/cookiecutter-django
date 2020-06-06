# pragma: no cover
"""
All the mixins that can be used in the system and for Django REST Framework Views
"""
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class AnonymousAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        return (request._request.user, None)


class BaseAuthView(permissions.BasePermission):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)


class BaseGetApiView(BaseAuthView, permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user and request.user.is_authenticated


class BaseGetPostPutApiView(BaseAuthView, permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET' or request.method == 'POST' or request.method == 'PUT':
            return True
        return request.user and request.user.is_authenticated


class BaseGetPostApiView(BaseAuthView, permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET' or request.method == 'POST':
            return True
        return request.user and request.user.is_authenticated


class BaseDestroyApiView(BaseAuthView):

    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return True
        return request.user and request.user.is_authenticated


class BasePostApiView(BaseAuthView):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user and request.user.is_authenticated


class BasePutApiView(BaseAuthView):

    def has_permission(self, request, view):
        if request.method == 'PUT':
            return True
        return request.user and request.user.is_authenticated


class BaseUpdateApiView(BaseAuthView):

    def has_permission(self, request, view):
        if request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH':
            return True
        return request.user and request.user.is_authenticated


class BaseUpdateAndDestroyApiView(BaseAuthView):

    def has_permission(self, request, view):
        if request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH' or request.method == 'DELETE':
            return True
        return request.user and request.user.is_authenticated


class BaseCRUDApiView(BaseAuthView):

    def has_permission(self, request, view):
        if request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH' or request.method == 'GET' \
                or request.method == 'DELETE':
            return True
        return request.user and request.user.is_authenticated


class BaseGetPostAndDestroyApiView(BaseAuthView):

    def has_permission(self, request, view):
        if request.method == 'POST' or request.method == 'GET' or request.method == 'DELETE':
            return True
        return request.user and request.user.is_authenticated


class BaseGetPutPatchApiView(BaseAuthView):

    def has_permission(self, request, view):
        if request.method == 'GET' or request.method == 'PUT' or request.method == 'PATCH':
            return True
        return request.user and request.user.is_authenticated


class BaseGetPutPostPatchApiView(BaseAuthView):

    def has_permission(self, request, view):
        if request.method == 'GET' or request.method == 'PUT' or request.method == 'POST' or request.method == 'PATCH':
            return True
        return request.user and request.user.is_authenticated


class BaseGetDestroyApiView(BaseAuthView):
    def has_permission(self, request, view):
        if request.method == 'GET' or request.method == 'DELETE':
            return True
        return request.user and request.user.is_authenticated


class BaseGetPutPostDestroyApiView(BaseAuthView):

    def has_permission(self, request, view):
        if request.method == 'GET' or request.method == 'PUT' or request.method == 'POST' or request.method == 'DELETE':
            return True
        return request.user and request.user.is_authenticated


class BasePutPostDestroyApiView(BaseAuthView):

    def has_permission(self, request, view):
        if request.method == 'PUT' or request.method == 'POST' or request.method == 'DELETE':
            return True
        return request.user and request.user.is_authenticated
