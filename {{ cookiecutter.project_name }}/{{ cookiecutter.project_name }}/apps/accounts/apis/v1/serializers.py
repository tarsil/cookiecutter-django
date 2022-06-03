import logging
import re

import accounts.models
import bleach
from core.constants import BLACKLISTED_DOMAINS
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, update_last_login
from django.db import IntegrityError, OperationalError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

log = logging.getLogger(__name__)


class EmailTokenObtainSerializer(TokenObtainSerializer):
    username_field = User.EMAIL_FIELD
    default_error_messages = {"no_active_account": _("No account found with the given credentials")}


class CustomTokenObtainPairSerializer(EmailTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer that creates a HubUser in the system"""

    first_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    retype_password = serializers.CharField(required=True, allow_null=False, allow_blank=False)

    class Meta:
        model = accounts.models.HubUser
        fields = ("first_name", "last_name", "email", "password", "retype_password")

    def check_email_domain_is_valid(self, email):
        if email.split("@")[-1].strip() in BLACKLISTED_DOMAINS:
            return False
        return True

    def validate_email(self, email):
        hub_user = accounts.models.HubUser.objects.filter(user__email__iexact=email.strip())
        if hub_user.exists():
            raise serializers.ValidationError(_("This email is already registered in our system"))
        if not self.check_email_domain_is_valid(email):
            raise serializers.ValidationError(_("This email address is invalid"))
        return email

    def validate(self, attrs):
        try:
            password = attrs["password"]
            retype_password = attrs["retype_password"]

            if password != retype_password:
                raise serializers.ValidationError({"password": _("The passwords don't match")})

        except (ValueError, KeyError):
            raise serializers.ValidationError(_("Something went wrong, please reload the page and try again"))

        return attrs

    def create(self, validated_data):
        """Creates an HubUser in the system. This by default sets the incomplete_signup = True
        Removes dota that we don't need and inserts the rest

        """
        try:
            validated_data.pop("retype_password")
            validated_data.update(
                {
                    "first_name": bleach.clean(validated_data["first_name"]),
                    "last_name": bleach.clean(validated_data["last_name"]),
                    "email": bleach.clean(validated_data["email"].strip()),
                }
            )
            instance = accounts.models.HubUser.create_hub_user(**validated_data)
            return instance
        except IntegrityError:
            log.exception("Something went wrong whilst creating the account")
            raise serializers.ValidationError(_("Something happened while creating the account"))


class UpdateEmailSerializer(serializers.Serializer):
    """Renders and validates the email update serializer"""

    email = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    new_email = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    confirm_email = serializers.CharField(required=True, allow_null=False, allow_blank=False)

    def check_email_domain_is_valid(self, email):
        if email.split("@")[-1].strip() in BLACKLISTED_DOMAINS:
            return False
        return True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hub_user = self.context.get("hub_user")

    def is_user_email(self, email):
        if email.strip() == self.hub_user.user.email:
            return True
        return False

    def validate_email(self, email):
        if not email:
            raise serializers.ValidationError(_("Email cannot be empty"))
        if not self.is_user_email(email):
            raise serializers.ValidationError(_("This email does not match your current email account"))
        if not self.check_email_domain_is_valid(email):
            raise serializers.ValidationError(_("This email address is invalid."))
        return email

    def validate_new_email(self, new_email):
        if not new_email:
            raise serializers.ValidationError(_("Email cannot be empty"))

        if get_user_model().objects.filter(email__iexact=new_email).exclude(hub_user=self.hub_user).exists():
            raise serializers.ValidationError(_("This email already matches with a different account"))

        if self.is_user_email(new_email):
            raise serializers.ValidationError(_("This email is the same as your current account"))
        if not self.check_email_domain_is_valid(new_email):
            raise serializers.ValidationError(_("This email address is invalid."))
        return new_email

    def validate_confirm_email(self, confirm_email):
        if get_user_model().objects.filter(email__iexact=confirm_email).exclude(hub_user=self.hub_user).exists():
            raise serializers.ValidationError(_("This email already matches with a different account"))

        if self.is_user_email(confirm_email):
            raise serializers.ValidationError(_("This email is the same as your current account"))
        if not self.check_email_domain_is_valid(confirm_email):
            raise serializers.ValidationError(_("This email address is invalid."))
        return confirm_email

    def validate(self, attrs):
        new_email = attrs.get("new_email").strip()
        confirm_email = attrs.get("confirm_email").strip()

        if new_email != confirm_email:
            raise serializers.ValidationError(
                {"new_email": _("The emails do not match"), "confirm_email": _("The emails do not match")}
            )
        return attrs

    def update(self, instance, validated_data):
        instance = accounts.models.HubUser.update_email(instance, validated_data.get("new_email"))
        return instance


class UpdatePasswordSerializer(serializers.Serializer):
    """ """

    password = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    new_password = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    confirm_password = serializers.CharField(required=True, allow_blank=False, allow_null=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hub_user = self.context.get("hub_user")

    def check_password(self, password):
        """Validates the regex for a password.
        Minimum eight characters, at least one uppercase letter, one lowercase letter,
        one number and one special character, no blood of a virgin is required!
        """
        if re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password):
            return True
        return False

    def is_hub_user_password(self, password):
        return self.instance.check_password(password)

    def validate_password(self, password):
        if not self.is_hub_user_password(password):
            raise serializers.ValidationError(_("This password doesn't match the current password"))
        return password

    def validate_new_password(self, new_password):
        if self.is_hub_user_password(new_password):
            raise serializers.ValidationError(_("The password is the same as the original"))
        return new_password

    def validate_confirm_password(self, confirm_password):
        if self.is_hub_user_password(confirm_password):
            raise serializers.ValidationError(_("The password is the same as the original"))
        return confirm_password

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        if not new_password == confirm_password:
            raise serializers.ValidationError(
                {"new_password": _("The passwords do not match"), "confirm_password": _("The passwords do not match")}
            )
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get("new_password"))
        instance.save()
        return instance


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
