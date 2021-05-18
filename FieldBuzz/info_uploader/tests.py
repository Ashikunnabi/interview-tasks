from django.test import TestCase, Client
from .models import *
from .views import *
from django.core.exceptions import ValidationError
from django.urls import reverse, resolve


# Test models
class TestModelAuthToken(TestCase):
    """Test cases for AuthToken model"""

    def setUp(self) -> None:
        AuthToken.objects.create(
            token='sger654gjt8793bgfmyu#G$%$65yergew5',
            is_valid=True
        )

    def test_create_auth_token_instance(self) -> None:
        auth_token = AuthToken.objects.create(
            token='sger654gjt8793bgfmyu#G$%$65yergew5',
            is_valid=True
        )
        # created at unix timestamp in millisecond check
        self.assertEqual(len(str(auth_token.created_at)), 13)
        # created_at and updated_at is equal
        self.assertEqual(auth_token.created_at, auth_token.updated_at)

    def test_update_auth_token_instance(self) -> None:
        auth_token = AuthToken.objects.get(id=1)
        # update is_valid field
        auth_token.is_valid = False
        time.sleep(1)
        auth_token.save()
        # created_at and updated_at is not equal
        self.assertNotEqual(auth_token.created_at, auth_token.updated_at)


class TestModelPersonalInformation(TestCase):
    """Test cases for PersonalInformation model"""

    def setUp(self) -> None:
        PersonalInformation.objects.create(
            name='Alex',
            email='alex@gmail.com',
            phone='01896385274',
            full_address='Bangladesh',
            name_of_university='Test University',
            graduation_year=2020,
            cgpa=4.0,
            experience_in_months=10,
            current_work_place_name='Test Work Place',
            applying_in='Backend',
            expected_salary=20000,
            field_buzz_reference='',
            github_project_url='http://github.com',
            cv_file="""{"tsync_id": "try6547rhg678ufdger6543"}""",
            cv_file_path='media/test',
        )

    def test_instance_creation_successful(self) -> None:
        personal_information = PersonalInformation.objects.get(id=1)
        self.assertIsInstance(personal_information, PersonalInformation)

    def test_graduation_year_in_between_2015_to_2020(self) -> None:
        personal_information = PersonalInformation.objects.get(id=1)
        # check graduation_year less than 2015
        personal_information.graduation_year = 2014
        try:
            personal_information.full_clean()
        except Exception as ex:
            self.assertEqual(ex.__str__(),
                             "{'graduation_year': ['Ensure this value is greater than or equal to 2015.']}")
        else:
            # Validation is ok we will save the instance
            personal_information.save()

        # check graduation_year grater than 2020
        personal_information.graduation_year = 2021
        try:
            personal_information.full_clean()
        except ValidationError as ex:
            self.assertEqual(ex.__str__(), "{'graduation_year': ['Ensure this value is less than or equal to 2020.']}")
        else:
            # Validation is ok we will save the instance
            personal_information.save()

        # check graduation_year in between 2015 to 2020
        personal_information.graduation_year = 2017
        personal_information.full_clean()
        # Validation is ok we will save the instance
        personal_information.save()
        self.assertEqual(personal_information.graduation_year, 2017)

    def test_cgpa_in_between_2_to_4(self) -> None:
        personal_information = PersonalInformation.objects.get(id=1)
        # check cgpa less than 2.0
        personal_information.cgpa = 1.9
        try:
            personal_information.full_clean()
        except ValidationError as ex:
            self.assertEqual(ex.__str__(), "{'cgpa': ['Ensure this value is greater than or equal to 2.0.']}")
        else:
            # Validation is ok we will save the instance
            personal_information.save()

        # check cgpa grater than 2020
        personal_information.cgpa = 4.1
        try:
            personal_information.full_clean()
        except ValidationError as ex:
            self.assertEqual(ex.__str__(), "{'cgpa': ['Ensure this value is less than or equal to 4.0.']}")
        else:
            # Validation is ok we will save the instance
            personal_information.save()

        # check cgpa in between  2.0 to 4.0
        personal_information.cgpa = 3.1
        personal_information.full_clean()
        # Validation is ok we will save the instance
        personal_information.save()
        self.assertEqual(personal_information.cgpa, 3.1)

    def test_experience_in_months_in_between_0_to_100(self) -> None:
        personal_information = PersonalInformation.objects.get(id=1)
        # check experience_in_months less than 0
        personal_information.experience_in_months = -1
        try:
            personal_information.full_clean()
        except ValidationError as ex:
            self.assertEqual(ex.__str__(),
                             "{'experience_in_months': ['Ensure this value is greater than or equal to 0.']}")
        else:
            # Validation is ok we will save the instance
            personal_information.save()

        # check experience_in_months grater than 100
        personal_information.experience_in_months = 101
        try:
            personal_information.full_clean()
        except ValidationError as ex:
            self.assertEqual(ex.__str__(),
                             "{'experience_in_months': ['Ensure this value is less than or equal to 100.']}")
        else:
            # Validation is ok we will save the instance
            personal_information.save()

        # check experience_in_months in between 0 to 100
        personal_information.experience_in_months = 99
        personal_information.full_clean()
        # Validation is ok we will save the instance
        personal_information.save()
        self.assertEqual(personal_information.experience_in_months, 99)

    def test_expected_salary_in_between_15000_to_60000(self) -> None:
        personal_information = PersonalInformation.objects.get(id=1)
        # check expected_salary less than 15000
        personal_information.expected_salary = 14999
        try:
            personal_information.full_clean()
        except ValidationError as ex:
            self.assertEqual(ex.__str__(),
                             "{'expected_salary': ['Ensure this value is greater than or equal to 15000.']}")
        else:
            # Validation is ok we will save the instance
            personal_information.save()

        # check expected_salary grater than 60000
        personal_information.expected_salary = 60001
        try:
            personal_information.full_clean()
        except ValidationError as ex:
            self.assertEqual(ex.__str__(), "{'expected_salary': ['Ensure this value is less than or equal to 60000.']}")
        else:
            # Validation is ok we will save the instance
            personal_information.save()

        # check experience_in_months in between 15000 to 60000
        personal_information.expected_salary = 59999
        personal_information.full_clean()
        # Validation is ok we will save the instance
        personal_information.save()
        self.assertEqual(personal_information.expected_salary, 59999)

    def test_cv_file_contains_tsync_id(self) -> None:
        personal_information = PersonalInformation.objects.get(id=1)
        personal_information.cv_file = """{"sync_id": "try6547rhg678ufdger6543"}"""
        try:
            personal_information.full_clean()
        except ValidationError as ex:
            self.assertEqual(ex.__str__(), '{\'cv_file\': ["JSON key \'tsync_id\' is required."]}')
        else:
            # Validation is ok we will save the instance
            personal_information.save()


class TestUrlPersonalInformation(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_personal_information_get(self):
        response = self.client.get(reverse('personal_information'))
        # for a successful request, response status code will be 200
        self.assertEqual(response.status_code, 200)

        # check response contains proper html
        self.assertIn(b'<!DOCTYPE html>', response.content)
        self.assertIn(b'<title>An Interview Task</title>', response.content)

        # check template return
        self.assertTemplateUsed(response, 'info_uploader/index.html')

        # check proper function/class returns
        self.assertEqual(resolve(reverse('personal_information')).func.view_class, PersonalInformationView)
