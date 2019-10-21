from __future__ import unicode_literals
import bleach

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.contrib.auth.models import Permission as DjangoPermission
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_init, post_save
from django.db import models

from lib.cache.decorators import memoize_invalidate


class Choices(object):

    class Profiles:
        ADMIN = u'admin'
        USER = u'user'
        MANAGER = u'manager'
        OTHER = u'other'

        PROFILE_CHOICES = (
            (ADMIN, 'Admin'),
            (USER, 'User'),
            (MANAGER, 'Manager'),
            (OTHER, 'Other'),
        )


class ProfileType(models.Model):
    profile = models.ForeignKey('accounts.Profile', null=False, blank=True, related_name='profile_types',
                                on_delete=models.DO_NOTHING)
    profile_type = models.CharField(max_length=255, choices=Choices.Profiles.PROFILE_CHOICES,
                                    default=Choices.Profiles.USER, null=False, blank=False)

    def __str__(self):
        return self.get_profile_type_display()


class Profile(models.Model):
    """
    For every user, there is a profile associated. This model is a representation of that same profile
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='profile',
                                on_delete=models.DO_NOTHING)
    slug = models.SlugField(max_length=255, help_text=_('Slug'), blank=False, null=False, unique=True)
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    modified_at = models.DateTimeField(null=False, blank=False, auto_now=True)
    is_hidden = models.BooleanField(default=False, blank=False, null=False)
    is_disabled = models.BooleanField(default=False, blank=False, null=False)
    is_password_changed = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self):
        return self.slug


class User(AbstractUser):
    """
    Model responsible for the user maintenance for the platform
    """
    class Meta:
        db_table = 'auth_user'
        permissions = (('can_view_dashboard', 'Can view all dashboards'),
                       ('can_view_store_profiles', 'Can store profiles'),)

    @memoize_invalidate
    def get_or_create_profile(self, first_name=None, last_name=None):
        try:
            return Profile.objects.get(user=self)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(
                user=self, slug=self.username
            )
            profile.save()
            return profile

    def to_json_dict(self, context=None):
        data = {
            'id': self.pk,
            'username': bleach.clean(self.username),
            'email_url': reverse('postman_write', args=(self.pk,))
        }

        profile = self.profile
        if profile is not None:
            data['profile'] = profile.to_json_dict(context)

        return data

    def get_primary_email(self):
        return self.email

    @staticmethod
    def post_init(sender, **kwargs):
        instance = kwargs["instance"]
        instance.first_name = bleach.clean(instance.first_name)
        instance.last_name = bleach.clean(instance.last_name)
        instance.old_email = instance.email
        instance.old_is_active = instance.is_active
        instance.old_first_name = instance.first_name
        instance.old_last_name = instance.last_name

    @staticmethod
    def post_save(sender, **kwargs):
        instance = kwargs["instance"]
        try:
            profile = instance.profile
        except Profile.DoesNotExist:
            pass
        instance.old_email = instance.email
        instance.old_first_name = instance.first_name
        instance.old_last_name = instance.last_name

    @property
    def display_name(self):
        return self.first_name + u' ' + self.last_name


post_init.connect(User.post_init, sender=User)
post_save.connect(User.post_save, sender=User)


class Permission(DjangoPermission):

    class Meta:
        proxy = True
        permissions = (
            ('shorten_urls', 'Can shorten urls anywhere'),
        )
