from django_webtest import WebTest
from django.urls import reverse

import accounts.tests.factories
import accounts.models


class LoginAndRegisterViewTest(WebTest):

    def setUp(self):
        self.user = accounts.tests.factories.UserFactory(username=u'{{ project_name }}', email="cenas@cenas.com")
        self.url_login = reverse('login')

    def test_get_login_page(self):
        response = self.app.get(self.url_login)

        self.assertEqual(200, response.status_code)
