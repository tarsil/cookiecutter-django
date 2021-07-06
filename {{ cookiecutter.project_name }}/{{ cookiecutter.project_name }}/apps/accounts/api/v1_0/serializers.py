import bleach
import accounts.models

from django.contrib.auth import authenticate
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """Validates the login of a HubUser"""
    email = serializers.EmailField(allow_blank=False, required=True)
    password = serializers.CharField(allow_blank=False, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth_user = None

    def get_user(self):
        return self.auth_user

    def validate(self, attrs):
        try:
            email = attrs['email'].strip()
            password = attrs['password']
            try:
                self.auth_user = authenticate(email=bleach.clean(email), password=password)
            except ValueError:
                self.auth_user = None

            if self.auth_user:
                return attrs

        except (accounts.models.HubUser.DoesNotExist, KeyError):
            pass
        raise serializers.ValidationError(_("Your login details were incorrect. Please try again."))
