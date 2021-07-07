from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

import accounts.models
import accounts.tests.factories


class BaseTest(TestCase):

    def teardown(self):
        get_user_model().objects.all().delete()
        accounts.models.HubUser.objects.all().delete()


class UserAccountModelTest(BaseTest):

    def setUp(self):
        self.user = accounts.tests.factories.UserFactory(username='stuff')
        self.user_2 = accounts.tests.factories.UserFactory(username='{{ cookiecutter.project_name }}_2')

    def test_create_user(self):
        self.assertEqual('stuff', self.user.username)

    def test_create_user_with_specific_email(self):
        self.user.email = '{{ cookiecutter.project_name }}@test.com'
        self.user.save()

        self.assertEqual(self.user.email, '{{ cookiecutter.project_name }}@test.com')

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


class AccountModelTest(BaseTest):

    def setUp(self) -> None:
        get_user_model().objects.all().delete()
        accounts.models.HubUser.objects.all().delete()

    def test_can_create_user_model(self):
        """Tests if can create a Django User Model"""
        user = accounts.tests.factories.UserFactory()
        self.assertIsNotNone(user)

    def test_cant_create_more_than_one_user(self):
        """Tests the possibility of creating more than one Django User Model"""
        for i in range(5):
            accounts.tests.factories.UserFactory()

        users = get_user_model().objects.all()

        self.assertEqual(5, users.count())

    def test_creates_a_user_and_profiles_and_hub(self):
        """Tests using the create_hub_user successfully"""
        accounts.models.HubUser.create_hub_user('{{ cookiecutter.project_name }}@test.com', '123test', 'User', username='test_user',
                                                first_name='first', last_name='last')

        users = get_user_model().objects.all()
        hub_users = accounts.models.HubUser.objects.all()

        self.assertEqual(users.count(), 1)
        self.assertEqual(hub_users.count(), 1)

    def test_information_created_matches(self):
        """The information created on cascade matches"""
        accounts.models.HubUser.create_hub_user('{{ cookiecutter.project_name }}@test.com', '123test', 'User', username='test_user',
                                                first_name='first', last_name='last')

        users = get_user_model().objects.all()
        hub_users = accounts.models.HubUser.objects.all()

        user = users[0]
        hub_user = hub_users[0]

        self.assertEqual(user.username, 'test_user')
        self.assertEqual(user.email, '{{ cookiecutter.project_name }}@test.com')
        self.assertEqual(hub_user.user.pk, user.pk)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password('123test'))


class HubUserDetailsModelTest(TestCase):

    def setUp(self) -> None:
        self.hub_user = accounts.tests.factories.HubUserFactory()

    def tearDown(self) -> None:
        get_user_model().objects.all().delete()
        accounts.models.HubUser.objects.all().delete()

    def test_can_create_profile(self):
        """Tests the creation of a profile successfully"""
        self.assertIsNotNone(self.hub_user)

    def test_can_create_profile_and_is_only_one(self):
        """Tests the creation of a profile successfully and only one"""
        total = accounts.models.HubUser.objects.all()

        self.assertEqual(total.count(), 1)
        self.assertIsNotNone(self.hub_user)
