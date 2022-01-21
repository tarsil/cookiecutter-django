# -*- coding: utf-8 -*-
"""
Management utility to create superusers.
"""
from django.core import exceptions
from typing import Optional, Any
import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.management.commands.createsuperuser import Command as CreateSuperUserCommand

from accounts.models import HubUser, Choices


class Command(CreateSuperUserCommand):
    help = "Used to create a superuser by extending the current Command."
    requires_migrations_checks = True
    stealth_options = ("stdin",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_data = {
            'username': None,
            'email': None
        }

    def get_input_data(self, field, message, default=None):
        """
        Override this method if you want to customize data inputs or
        validation exceptions.

        Extends the input data to create an independent dictionary
        and populate the `self.user_data`.
        """
        raw_value = input(message)
        if default and raw_value == '':
            raw_value = default
        try:
            val = field.clean(raw_value, None)
        except exceptions.ValidationError as e:
            self.stderr.write("Error: %s" % '; '.join(e.messages))
            val = None

        if field.name == 'username':
            self.user_data[field.name] = val
        elif field.name == 'email':
            self.user_data[field.name] = val
        return val

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        """
        Extends the handle and creates the HubUser for the system.
        """
        super().handle(*args, **options)
        self.generate_profile_from_user()

    def generate_profile_from_user(self):
        from slugify import slugify

        user = get_user_model().objects.get(email=self.user_data.get("email"))
        user.first_name = "User"
        user.last_name = "Administrator"
        user.save()

        # CREATE USER
        HubUser.objects.create(
            user=user, slug=slugify(user.username), uuid=str(uuid.uuid4()), profile_type=Choices.Profiles.ADMIN
        )
