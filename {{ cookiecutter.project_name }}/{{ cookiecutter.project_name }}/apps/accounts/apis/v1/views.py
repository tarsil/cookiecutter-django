import logging

import accounts.apis.v1.serializers
import accounts.models
import bleach
from accounts.apis.v1.serializers import (
    CustomTokenObtainPairSerializer, 
    UpdatePasswordSerializer,
    UpdateEmailSerializer,
    UserRegistrationSerializer
)
from django.contrib.auth import login
from django.db import IntegrityError, OperationalError, transaction
from django.urls import reverse
from lib.{{cookiecutter.project_name}}.rest.generics import AuthMixin, RequiredUserContextView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import DestroyAPIView, RetrieveAPIView, UpdateAPIView

log = logging.getLogger(__name__)


class EmailTokenObtainPairView(TokenObtainPairView):
    """
    Replaces the token get from username and adds the possibility to be as email.
    """

    serializer_class = CustomTokenObtainPairSerializer


class RegisterApiView(APIView):
    """Registers a HubUser in the platform"""

    serializer_class = UserRegistrationSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class BaseUpdateUser(AuthMixin, RequiredUserContextView):
    """Base for the updates of the HubUser"""

    def get_object(self):
        return self.request.user


class UpdatePasswordView(BaseUpdateUser, UpdateAPIView):
    """From the HubUser settings page, updates the password"""

    serializer_class = UpdatePasswordSerializer

    def update(self, request, *args, **kwargs):
        """Updates current password of the account
        1. Check if the password is the same as the hub user
        2. Check if the passwords provided match
        3. Updates
        """
        instance = self.get_object()
        serializer = self.serializer_class(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class UpdateEmailView(BaseUpdateUser, UpdateAPIView):
    """Updates the email of an HubUser"""

    serializer_class = UpdateEmailSerializer

    def update(self, request, *args, **kwargs):
        """Updates current email of the account
        1. Check if the email is the same as the hub user
        2. Check if the emails provided match
        3. Updates

        """
        instance = self.get_object()
        serializer = self.serializer_class(instance=instance, data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(status=status.HTTP_200_OK)


class DeleteUserAccountApiView(AuthMixin, DestroyAPIView):
    """View for the right to be forgotten and to remove the account for good"""
    def destroy(self, request, *args, **kwargs):
        instance = self.request.user
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginApiView(APIView):
    """View handling with the Login System via API"""
    serializer_class = accounts.apis.v1.serializers.LoginSerializer
    redirect_url = None

    def get_success_url(self):
        """ """
        redirect_url = self.request.data.get('next', '')
        redirect_url = bleach.clean(redirect_url)
        if not redirect_url:
            return reverse('homepage')
        return redirect_url

    def post(self, request, *args, **kwargs):
        """Gets the data from the request and validates against a record in the database
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # CREATE LOGIN
        user = serializer.get_user()
        login(request, user)

        # SET THE STATUS TO ONLINE
        accounts.utils.set_status(user.hub_user, accounts.models.Choices.ProfileStatus.ONLINE)
        return Response({'url': self.get_success_url()}, status=status.HTTP_200_OK)
