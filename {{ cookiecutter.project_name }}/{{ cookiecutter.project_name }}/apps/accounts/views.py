import accounts.models
import bleach
from django.contrib.auth import login
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import accounts.serializers


class LoginApiView(APIView):
    """View handling with the Login System via API"""
    serializer_class = accounts.serializers.LoginSerializer
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
