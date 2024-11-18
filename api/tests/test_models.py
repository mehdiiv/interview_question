import jwt
from django.test import TestCase
from decouple import config
from api.models import User

JWT_SECRET_KEY = config('JWT_SECRET_KEY')


def create_jwt(email):

    return jwt.encode({'email': email}, JWT_SECRET_KEY, algorithm="HS256")


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@test.com', json_web_token=create_jwt('test@test.com')
        )

    def test_model_user_cerate(self):
        self.assertEqual(self.user.email, 'test@test.com')
        self.assertEqual(self.user.json_web_token, create_jwt('test@test.com'))

    def test_user_table_name(self):
        self.assertEqual(self.user._meta.db_table, 'users')
