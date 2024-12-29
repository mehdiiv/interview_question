from django.test import SimpleTestCase
from django.urls import reverse, resolve
from api.users import UsersView
from api.messages import MessagesViews


class UrlTest(SimpleTestCase):
    def test_users_url(self):
        url = reverse('users')
        self.assertEqual(resolve(url).func.view_class, UsersView)

    def test_messages_url(self):
        url = reverse('messages')
        self.assertEqual(resolve(url).func.view_class, MessagesViews)
