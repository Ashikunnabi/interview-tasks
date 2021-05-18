from django.test import TestCase, Client
from django.urls import reverse
import json


class TestViewsets(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_list_url = 'user-list'
        self.user_detail_url = 'user-detail'

    def test_create_user(self):
        response = self.client.post(reverse(self.user_list_url), {
            'first_name': 'Parent',
            'last_name': '1',
            'street': 'Gorib-A-Newaz Aveneu',
            'city': 'Dhaka',
            'state': 'Dhaka',
            'zip': '1230'
        })
        self.assertEquals(response.status_code, 201)
        self.assertEqual(json.loads(response.content)['first_name'], 'Parent')

    def test_create_child_check_parent_required(self):
        # parent user
        self.client.post(reverse(self.user_list_url), {
            'first_name': 'Parent',
            'last_name': '1',
            'street': 'Gorib-A-Newaz Aveneu',
            'city': 'Dhaka',
            'state': 'Dhaka',
            'zip': '1230'
        })
        # child user
        response = self.client.post(reverse(self.user_list_url), {
            'first_name': 'Child',
            'last_name': '1',
            'is_child': 1,
            # 'parent': 1,
            'street': 'Gorib-A-Newaz Aveneu',
            'city': 'Dhaka',
            'state': 'Dhaka',
            'zip': '1230'
        })
        self.assertEquals(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['non_field_errors'], [
                         'Parent is required for this user.'])

    def test_update_user(self):
        # new user instance create
        response = self.client.post(reverse(self.user_list_url), {
            'first_name': 'Parent',
            'last_name': '1',
            'street': 'Gorib-A-Newaz Aveneu',
            'city': 'Dhaka',
            'state': 'Dhaka',
            'zip': '1230'
        })

        # update user instance
        response = self.client.patch(reverse(self.user_detail_url, args=['1']),
                                     json.dumps({'last_name': 'One'}),
                                     content_type='application/json')
        self.assertEquals(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['last_name'], 'One')

    def test_user_count(self):
        # creating 2 user instance
        self.client.post(reverse(self.user_list_url), {
            'first_name': 'Parent',
            'last_name': '1',
            'street': 'Gorib-A-Newaz Aveneu',
            'city': 'Dhaka',
            'state': 'Dhaka',
            'zip': '1230'
        })

        self.client.post(reverse(self.user_list_url), {
            'first_name': 'Child',
            'last_name': '1',
            'is_child': True,
            'parent': 1,
            'street': 'Gorib-A-Newaz Aveneu',
            'city': 'Dhaka',
            'state': 'Dhaka',
            'zip': '1230'
        })
        # call user-list api
        response = self.client.get(reverse(self.user_list_url))
        self.assertEqual(len(json.loads(response.content)), 2)

    def test_user_delete_parent(self):
        # creating 2 user instance
        self.client.post(reverse(self.user_list_url), {
            'first_name': 'Parent',
            'last_name': '1',
            'street': 'Gorib-A-Newaz Aveneu',
            'city': 'Dhaka',
            'state': 'Dhaka',
            'zip': '1230'
        })

        self.client.post(reverse(self.user_list_url), {
            'first_name': 'Child',
            'last_name': '1',
            'is_child': True,
            'parent': 1,
            'street': 'Gorib-A-Newaz Aveneu',
            'city': 'Dhaka',
            'state': 'Dhaka',
            'zip': '1230'
        })
        # delete parent
        self.client.delete(reverse(self.user_detail_url, args=[1]))
        # call user-list api
        response = self.client.get(reverse(self.user_list_url))
        # as parent deleted so child will also auto delete
        self.assertEqual(len(json.loads(response.content)), 0)

    def test_user_delete_child(self):
        # creating 2 user instance
        self.client.post(reverse(self.user_list_url), {
            'first_name': 'Parent',
            'last_name': '1',
            'street': 'Gorib-A-Newaz Aveneu',
            'city': 'Dhaka',
            'state': 'Dhaka',
            'zip': '1230'
        })

        self.client.post(reverse(self.user_list_url), {
            'first_name': 'Child',
            'last_name': '1',
            'is_child': True,
            'parent': 1,
            'street': 'Gorib-A-Newaz Aveneu',
            'city': 'Dhaka',
            'state': 'Dhaka',
            'zip': '1230'
        })
        # delete child
        self.client.delete(reverse(self.user_detail_url, args=[2]))
        # call user-list api
        response = self.client.get(reverse(self.user_list_url))
        self.assertEqual(len(json.loads(response.content)), 1)
