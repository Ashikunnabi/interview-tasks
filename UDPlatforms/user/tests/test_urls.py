from django.test import SimpleTestCase
from django.urls import reverse, resolve
from user.views import UserView


class TestUrls(SimpleTestCase):

    def test_users_url_is_resolved(self):
        url = reverse('users')
        self.assertEquals(resolve(url).func.view_class, UserView)
