from django.test import TestCase, Client
from django.urls import reverse
from decouple import config
from api.models import User
import json
from api.common_methods import create_jwt

JWT_SECRET_KEY = config('JWT_SECRET_KEY')


class ApiTest(TestCase):
    def setUp(self):
        create_jwt(email='test@test.com')
        self.user = User.objects.create(
            email='test@test.com',
            json_web_token=create_jwt('test@test.com')
        )
        self.client = Client()
        self.json_request = {'content_type': 'application/json'}

    def test_api_user_create(self):
        response = self.client.post(
            reverse('users'),
            json.dumps({"email": "test@test1.com"}),
            **self.json_request
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('email'), 'test@test1.com')

    def test_api_user_create_invalid_data_invalid_json(self):
        response = self.client.post(
            reverse('users'),
            json.dumps({"email": "test@test1.com"}) + 'sd',
            **self.json_request
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()['error_message'], 'invalid json')

    def test_api_user_create_wrong_date(self):
        self.api_user_create_invalid_data_null_mail()
        self.api_user_create_invalid_data_exist_mail()
        self.api_user_create_invalid_data_exist_empty_srting()
        self.api_user_create_invalid_data_inccorect_mail()

    def api_user_create_invalid_data_null_mail(self):
        response = self.client.post(
            reverse('users'),
            json.dumps({"email": None}),
            **self.json_request
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json()['error_message'],
            'email cannot be empty'
        )

    def api_user_create_invalid_data_exist_mail(self):
        response = self.client.post(
            reverse('users'),
            json.dumps({"email": 'test@test.com'}),
            **self.json_request
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json()['error_message'],
            'email alredy exist'
        )

    def api_user_create_invalid_data_exist_empty_srting(self):
        response = self.client.post(
            reverse('users'),
            json.dumps({"email": ''}),
            **self.json_request
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json()['error_message'],
            'email cannot be empty'
        )

    def api_user_create_invalid_data_inccorect_mail(self):
        response = self.client.post(
            reverse('users'),
            json.dumps({"email": 'test@test'}),
            **self.json_request
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json()['error_message'],
            'email is incorrect'
        )
