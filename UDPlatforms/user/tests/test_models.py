from django.test import TestCase
from user.models import User


class TestModels(TestCase):

    def setUp(self):
        self.parent = User.objects.create(
            first_name='Parent',
            last_name='1',
            street='Gorib-A-Newaz Aveneu',
            city='Dhaka',
            state='Dhaka',
            zip='1230'
        )
        self.child = User.objects.create(
            first_name='Parent',
            last_name='1',
            is_child=True,
            parent=User.objects.get(id=1),
            street='Gorib-A-Newaz Aveneu',
            city='Dhaka',
            state='Dhaka',
            zip='1230'
        )

    def test_count_user(self):
        self.assertEqual(User.objects.count(), 2)

    def test_child_will_not_contain_address(self):
        self.assertEqual(self.child.street, '')
        self.assertEqual(self.child.city, '')
        self.assertEqual(self.child.state, '')
        self.assertEqual(self.child.zip, '')

    def test_child_must_have_parent(self):
        self.assertIsNotNone(self.child.parent)
