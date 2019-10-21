# -*- coding: utf-8 -*-
from django.test import TestCase
from slugify import slugify

import accounts.tests.factories
import accounts.utils


class UtilsTest(TestCase):

    def setUp(self):
        self.user = accounts.tests.factories.UserFactory(username=u'{{ project_name }}-pórto')

    def test_can_slugify_string(self):
        result = slugify(self.user.username)

        self.assertEqual(result, u'{{ project_name }}-porto')

    def test_can_update_profile_slug(self):
        profile = accounts.tests.factories.ProfileFactory(slug=u'slug!déstá-coisa')
        user = accounts.tests.factories.UserFactory(profile=profile, username=u'slug!déstá-coisa')
        slug_slugified = slugify(user.username)

        self.assertEqual(slug_slugified, u'slug-desta-coisa')

        profile_expected = accounts.utils.update_profile_slug(profile, user)
        user.username = profile.slug
        user.save()

        self.assertEqual(profile_expected.slug, u'slug-desta-coisa')
        self.assertEqual(profile_expected.slug, user.username)
        self.assertEqual(user.username, u'slug-desta-coisa')
