# -*- coding: utf-8 -*-
from django.test import TestCase
from slugify import slugify

import accounts.tests.factories
import accounts.utils
from accounts.models import HubUser


class UtilsTest(TestCase):

    def setUp(self):
        self.user = accounts.tests.factories.UserFactory(username='{{ cookiecutter.project_name }}-pórto')

    def test_can_slugify_string(self):
        result = slugify(self.user.username)

        self.assertEqual(result, '{{ cookiecutter.project_name }}-porto')

    def test_can_update_profile_slug(self):
        user = accounts.tests.factories.HubUserFactory(user__username='slug!déstá-coisa')
        slug_slugified = slugify(user.user.username)

        self.assertEqual(slug_slugified, 'slug-desta-coisa')

        profile_expected = accounts.utils.update_hub_user_slug(user)
        user.user.username = user.slug
        user.save()
        
        user = HubUser.objects.get(pk=user.pk)

        self.assertEqual(profile_expected.slug, 'slug-desta-coisa')
        self.assertEqual(profile_expected.slug, user.user.username)
        self.assertEqual(user.user.username, 'slug-desta-coisa')
