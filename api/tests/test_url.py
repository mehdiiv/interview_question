from django.test import SimpleTestCase
from django.urls import reverse, resolve
from api.users import UsersView


class UrlTest(SimpleTestCase):
    def test_users_url(self):
        url = reverse('users')
        self.assertEqual(resolve(url).func.view_class, UsersView)
