from django.test import TestCase, Client
from django.urls import reverse
from decouple import config
from api.models import User, Message
import json
from api.common_methods import create_jwt
import jwt

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
        self.message = Message.objects.create(
            user_id=self.user.id, title='testtiltle', body='testbody'
            )
        self.bearer_token = 'Bearer ' + create_jwt(self.user.email)

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

    def test_api_users_list_limit(self):
        User.objects.create(
            email='test3@test3.com',
            json_web_token=create_jwt('test3@test3.com')
            )
        User.objects.create(
            email='test2@test2.com',
            json_web_token=create_jwt('test2@test2.com')
              )
        response = self.client.get(
            reverse('users'),
            {'limit': 2, 'offset': '0'}
              )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.json().get('users')), 2
            )
        users_dic = []
        for item in response.json().get('users'):
            users_dic.append(item)
        self.assertEqual(len(users_dic), 2)

    def test_api_users_list_invalid_limit(self):
        User.objects.create(
            email='test3@test3.com',
            json_web_token=create_jwt('test3@test3.com')
        )
        User.objects.create(
            email='test2@test2.com',
            json_web_token=create_jwt('test2@test2.com')
        )
        response = self.client.get(
            reverse('users'),
            {'limit': 'sfsafa',  'offset': 'sdsd'}
         )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json().get('users')), 3)
        users_dic = []
        for item in response.json().get('users'):
            users_dic.append(item.get('id'))
        self.assertEqual(users_dic, [1, 2, 3])

    def test_api_message_create(self):
        response = self.client.post(
            reverse('messages'),
            json.dumps({"title": "testtitle2", "body": "testbody2"}),
            **self.json_request, headers={'Authorization': self.bearer_token}
            )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('title'), 'testtitle2')

    def test_api_message_create_wrong_date(self):
        self.api_message_create_invalid_data_invaldi_jwt()
        self.api_message_create_invalid_data_invaldi_not_exist_user()
        self.api_message_create_invalid_data_null_mail()
        self.api_message_create_invalid_data_empty_string_mail()
        self.api_message_create_invalid_json()
        self.api_message_create_invalid_empty_title()
        self.api_message_create_invalid_data_invaldi_without_jwt()

    def api_message_create_invalid_data_invaldi_jwt(self):
        response = self.client.post(
            reverse('messages'),
            json.dumps({"title": "testtitle2", "body": "testbody2"}),
            **self.json_request, headers={'Authorization': 'invalidjwt'}
              )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json()['error_message'], 'you are not authorised'
            )

    def api_message_create_invalid_data_invaldi_not_exist_user(self):
        response = self.client.post(
            reverse('messages'),
            json.dumps({"title": "testtitle2", "body": "testbody2"}),
            **self.json_request,
            headers={
                'Authorization': 'bearer ' + create_jwt('notexsit@test.test')
                }
            )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json()['error_message'], 'you are not authorised'
            )

    def api_message_create_invalid_data_invaldi_without_jwt(self):
        response = self.client.post(
            reverse('messages'),
            json.dumps({"title": "testtitle2", "body": "testbody2"}),
            **self.json_request
            )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json()['error_message'], 'you are not authorised'
            )

    def api_message_create_invalid_data_null_mail(self):
        response = self.client.post(
            reverse('messages'),
            json.dumps({"title": "testtitle2", "body": "testbody2"}),
            **self.json_request,
            headers={
                'Authorization': 'bearer ' + create_jwt(None)
                }
            )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json()['error_message'], 'you are not authorised'
              )

    def api_message_create_invalid_data_empty_string_mail(self):
        response = self.client.post(
            reverse('messages'),
            json.dumps({"title": "testtitle2", "body": "testbody2"}),
            **self.json_request,
            headers={'Authorization': 'bearer ' + create_jwt('')}
            )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json()['error_message'], 'you are not authorised'
            )

    def api_message_create_invalid_data_inccorect_mail(self):
        response = self.client.post(
            reverse('messages'),
            json.dumps({"title": "testtitle2", "body": "testbody2"}),
            **self.json_request,
            headers={'Authorization': 'bearer ' + create_jwt('asfasfasf')}
              )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json()['error_message'], 'email is incorrect'
            )

    def api_message_create_invalid_json(self):
        response = self.client.post(
            reverse('messages'),
            json.dumps({"title": "testtitle2", "body": "testbody2"})+'sfsf',
            **self.json_request,
            headers={'Authorization': self.bearer_token}
            )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()['error_message'], 'invalid json')

    def api_message_create_invalid_empty_title(self):
        response = self.client.post(
            reverse('messages'),
            json.dumps({"title": "", "body": "testbody2"}),
            **self.json_request,
            headers={'Authorization': self.bearer_token}
            )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json()['error_message'], 'title cannot be empty'
              )

    def test_api_list_messages(self):
        Message.objects.create(
            user_id=self.user.id,
            title='testtiltle2', body='testbody2'
            )
        Message.objects.create(
            user_id=self.user.id,
            title='testtiltle3', body='testbody3'
            )
        response = self.client.get(
            reverse('messages'),
            headers={'Authorization': self.bearer_token}
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.json().get('messages')), 3
            )
        self.assertEqual(
            response.json().get('messages')[2].get('body'), 'testbody3'
            )
        message_dic = []
        for item in response.json().get('messages'):
            message_dic.append(item.get('id'))
        self.assertEqual(message_dic, [1, 2, 3])

    def test_api_list_messages_query_params_search(self):
        Message.objects.create(
            user_id=self.user.id,
            title='testtiltle2', body='testbody2'
            )
        Message.objects.create(
            user_id=self.user.id,
            title='testtiltle3', body='testbody3'
            )
        response = self.client.get(
            reverse('messages'),
            {'search_by': 'body2'},
            headers={'Authorization': self.bearer_token}
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json().get('messages')[0].get('body'), 'testbody2'
            )
        message_dic = []
        for item in response.json().get('messages'):
            message_dic.append(item.get('id'))
        self.assertEqual(message_dic, [2])

    def test_api_list_messages_query_params(self):
        Message.objects.create(
            user_id=self.user.id,
            title='testtiltle2',
            body='testbody2'
            )
        Message.objects.create(
            user_id=self.user.id,
            title='testtiltle3', body='testbody3'
            )
        response = self.client.get(
            reverse('messages'),
            {'limit': '1', 'offset': '0'},
            headers={'Authorization': self.bearer_token}
            )
        self.assertEqual(response.status_code, 200)
        message_dic = []
        for item in response.json().get('messages'):
            message_dic.append(item)
        self.assertEqual(len(message_dic), 1)

    def test_api_list_messages_wrong_query(self):
        Message.objects.create(
            user_id=self.user.id,
            title='testtiltle2', body='testbody2'
            )
        Message.objects.create(
            user_id=self.user.id,
            title='testtiltle3', body='testbody3'
            )
        response = self.client.get(
            reverse('messages'), {'limit': 'sdsd', 'offset': 'dsds'},
            headers={'Authorization': self.bearer_token}
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.json().get('messages')), 3
            )
        self.assertEqual(
            response.json().get('messages')[2].get('body'), 'testbody3'
            )
        message_dic = []
        for item in response.json().get('messages'):
            message_dic.append(item.get('id'))
        self.assertEqual(message_dic, [1, 2, 3])
