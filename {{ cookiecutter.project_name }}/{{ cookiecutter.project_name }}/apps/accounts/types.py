"""
All the types used for the accounts are placed here.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class ProfileType(models.TextChoices):
    ADMIN = "admin", _("Administrator")
    USER = "user", _("User")
    VIEWER = "viewer", _("Viewer")
    OTHER = "other", _("Other")
