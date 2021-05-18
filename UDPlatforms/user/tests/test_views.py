from django.test import TestCase, Client
from django.urls import reverse
from user.views import UserView


class TestUserView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_url = reverse('users')
        self.user_view_get_template = 'user/user.html'

    def test_userview_GET(self):
        response = self.client.get(self.user_url)
        # check status code of successfull action.
        self.assertEqual(response.status_code, 200)

    def test_userview_class_name(self):
        response = self.client.get(self.user_url)
        # check view class of the returned response
        self.assertEquals(response.resolver_match.func.view_class, UserView)
        self.assertEquals(response.resolver_match.func.__name__,
                          UserView.as_view().__name__)

    def test_userview_template_name(self):
        response = self.client.get(self.user_url)
        # check templates returned by the response
        self.assertTemplateUsed(response, self.user_view_get_template)

    def test_userview_template_returns_correct_html(self):
        response = self.client.get(self.user_url)
        self.assertTrue(response.content.startswith(b'\n<!DOCTYPE html>'))
        self.assertIn(
            b'<title>Interview Task (User App)</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))
