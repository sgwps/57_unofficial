from urllib import request
from django.test import TestCase, RequestFactory
from . import views

class LogicTestCase(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test(self):
        request_dict = {'name': ['test_name'], 
                'surname': ['test_surname'], 
                'username': ['test_username1111'], 
                'email': ['test1111@email.com'], 
                'password': ['test_pass'], 
                'birth_date': ['2022-04-12'], 
                'gender': ['2'], 
                'is_student': ['on'], 
                'end_year': ['1980'], 
                'grade_letter': ['other'], 
                'custom_grade_letter': ['Г'], 
                'custom_profile': ['1'], 
                'is_teacher': ['on'], 
                'subject_1': ['on'], 
                'another_subject0': ['история'], 
                'another_subject1': ['АСТРОНОМИЯ']}
        request = self.factory.post(
            'signup', request_dict
        )
        response = views.BasicRegistration.as_view()(request)
        self.assertEqual(response.status_code, 200)
        
