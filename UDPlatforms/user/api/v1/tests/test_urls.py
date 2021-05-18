from django.test import SimpleTestCase
from django.urls import reverse, resolve
from user.api.v1.viewsets import UserViewSet
from user.models import User


class TestUserAPIUrls(SimpleTestCase):

    def test_user_api_list_url_is_resolved(self):
        url = reverse('user-list')
        self.assertEqual(resolve(url).func.__name__,
                         UserViewSet.__name__)

    def test_user_api_details_url_is_resolved(self):
        url = reverse('user-detail', args=['6'])
        self.assertEqual(resolve(url).func.__name__,
                         UserViewSet.__name__)
