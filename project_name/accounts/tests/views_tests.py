from django_webtest import WebTest
from django.core.urlresolvers import reverse

import accounts.tests.factories
import accounts.models
import {{ project_name }}.third_parties.blacklist_domains


class ListUsersViewTest(WebTest):

    def setUp(self):
        self.user = accounts.tests.factories.UserFactory(username=u'LTPLabs', email="cenas@cenas.com")
        self.url = reverse('profiles:list-users')

    def test_get_login_page(self):
        response = self.app.get(self.url, user=self.user)

        self.assertEqual(200, response.status_code)


class LoginAndRegisterViewTest(WebTest):

    def setUp(self):
        self.user = accounts.tests.factories.UserFactory(username=u'LTPLabs', email="cenas@cenas.com")
        self.url_login = reverse('login')

    def _get_profile_page_data(self):
        return reverse('profiles:view-profile', kwargs={
            'slug': self.user.profile.slug
        })

    def test_get_login_page(self):
        response = self.app.get(self.url_login)

        self.assertEqual(200, response.status_code)

    def test_can_get_the_profile_page_for_logged_user(self):
        response = self.app.get(self._get_profile_page_data(), user=self.user)

        self.assertEqual(200, response.status_code)


class AddUserViewTest(WebTest):
    def setUp(self):
        self.user = accounts.tests.factories.UserFactory(username=u'LTPLabs')
        self.url = reverse('profiles:add-user')

    def _get_user_form_data(self, email='testeFirst@testeLast.com'):
        page = self.app.get(self.url, user=self.user)
        form = page.forms[0]
        form['first_name'] = 'testeFirst'
        form['last_name'] = 'testeLast'
        form['email'] = email
        form['password'] = '12345678'
        form['retype_password'] = '12345678'
        form['profile_type'] = accounts.models.Choices.ProfileType.STORE_PROFILES
        response = form.submit()

        return page, response

    def test_can_get_to_the_add_view_page(self):
        page = self.app.get(self.url, user=self.user)

        self.assertEqual(200, page.status_code)

    def test_can_add_new_user(self):
        page, response = self._get_user_form_data()

        self.assertEqual(302, response.status_code)

    def test_user_added_has_correct_profile_type(self):
        page, response = self._get_user_form_data()
        profile_wanted = accounts.models.Profile.objects.get(slug=self.user.profile.slug)
        profile_wanted.profile_type = accounts.models.Choices.ProfileType.STORE_PROFILES
        profile_wanted.save()

        self.assertEqual(profile_wanted.slug, self.user.profile.slug)
        self.assertEqual(profile_wanted.profile_type, accounts.models.Choices.ProfileType.STORE_PROFILES)

    def test_add_users_with_same_email_fails(self):
        page, response = self._get_user_form_data()
        page_now, response_now = self._get_user_form_data()

        self.assertIn(u'There is already an account with that email address.', str(response_now.content))

    def test_add_user_without_fields_that_are_required(self):
        page = self.app.get(self.url, user=self.user)
        form = page.forms[0]
        form['first_name'] = '123'
        form['last_name'] = ''
        form['email'] = '123@456.com'
        form['password'] = '12345678'
        form['retype_password'] = ''
        form['profile_type'] = accounts.models.Choices.ProfileType.STORE_PROFILES
        response = form.submit()

        self.assertFormError(response, 'form', 'last_name', 'This field is required.')
        self.assertFormError(response, 'form', 'retype_password', 'This field is required.')

    def test_add_user_with_blacklisted_domain(self):
        b_list = {{ project_name }}.third_parties.blacklist_domains.BLACKLISTED_DOMAINS
        import random
        email = 'test@' + random.sample(b_list, 1)[0]
        page, response = self._get_user_form_data(email=email)

        self.assertIn(u'This email address is invalid.', str(response.content))

