# -*- coding: utf-8 -*-
from django.test import TestCase
from slugify import slugify

import accounts.tests.factories
import accounts.utils


class UtilsTest(TestCase):

    def setUp(self):
        self.user = accounts.tests.factories.UserFactory(username=u'{{ cookiecutter.project_name }}-pórto')

    def test_can_slugify_string(self):
        result = slugify(self.user.username)

        self.assertEqual(result, u'{{ cookiecutter.project_name }}-porto')

    def test_can_update_profile_slug(self):
        user = accounts.tests.factories.HubUserFactory(user__username=u'slug!déstá-coisa')
        slug_slugified = slugify(user.user.username)

        self.assertEqual(slug_slugified, u'slug-desta-coisa')

        profile_expected = accounts.utils.update_hub_user_slug(user)
        user.user.username = user.slug
        user.save()

        self.assertEqual(profile_expected.slug, u'slug-desta-coisa')
        self.assertEqual(profile_expected.slug, user.user.username)
        self.assertEqual(user.user.username, u'slug-desta-coisa')
