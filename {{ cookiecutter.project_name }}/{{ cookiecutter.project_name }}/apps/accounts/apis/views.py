from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.middleware import csrf
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer


def get_tokens_for_user(user):
    """
    Gets the token for a given user using JWT
    """
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }


class LoginJWTApiView(APIView):
    """
    User login
    """
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        """
        Gets an email and a password, sanitizes and log a user.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = Response()

        # GETS THE USER
        user = serializer.get_user()

        if user is None or not user:
            return Response({
                'detail': 'Invalid email or password.'
            }, status=status.HTTP_404_NOT_FOUND)

        # CHECK ACTIVE USER
        if not user.is_active:
            return Response({
                'detail': 'This account is not active.'
            }, status=status.HTTP_404_NOT_FOUND)

        data = get_tokens_for_user(user)
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=data["access"],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        # UPDATES CSRF
        csrf.get_token(request)
        response.data = data

        return response
