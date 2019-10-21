from django.test import TestCase

import accounts.tests.factories
import accounts.models


class UserAccountModelTest(TestCase):

    def setUp(self):
        self.user = accounts.tests.factories.UserFactory(username='stuff')
        self.user_2 = accounts.tests.factories.UserFactory(username='{{ project_name }}_2')

    def test_create_user(self):
        self.assertEqual('stuff', self.user.username)

    def test_create_user_with_specific_email(self):
        self.user.email = '{{ project_name }}@test.com'
        self.user.save()

        self.assertEqual(self.user.email, '{{ project_name }}@test.com')

    def test_create_user_with_specific_password(self):
        self.user.password = '123password'
        self.user.save()

        self.assertEqual(self.user.password, '123password')

    def test_create_user_with_staff_access(self):
        self.user.is_staff = True
        self.user.save()

        self.assertEqual(self.user.is_staff, True)

    def test_can_create_more_than_one_user_at_the_same_time(self):
        self.assertNotEqual(self.user, self.user_2)


class ProfileTypeTests(TestCase):

    def setUp(self):
        self.profile = accounts.tests.factories.ProfileFactory()
        self.profile_type = accounts.tests.factories.ProfileTypeFactory()

    def test_can_create_profile_type_object(self):
        self.profile_type.profile_type = accounts.models.Choices.Profiles.ADMIN
        self.profile_type.save()

        self.assertEqual(self.profile_type.profile_type, accounts.models.Choices.Profiles.ADMIN)

    def test_can_have_multiple_profile_types(self):

        accounts.tests.factories.ProfileTypeFactory(
            profile=self.profile,
            profile_type=accounts.models.Choices.Profiles.USER
        )

        accounts.tests.factories.ProfileTypeFactory(
            profile=self.profile,
            profile_type=accounts.models.Choices.Profiles.ADMIN
        )

        profiles = accounts.models.ProfileType.objects.filter(
            profile=self.profile
        )

        self.assertEqual(profiles.count(), 2)
