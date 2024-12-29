from django.http import JsonResponse
from decouple import config
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import jwt
import json

JWT_SECRET_KEY = config('JWT_SECRET_KEY')


def create_jwt(email):

    return jwt.encode({'email': email}, JWT_SECRET_KEY, algorithm="HS256")


def fetch_data(json_data):
    try:
        return False, json.loads(json_data)
    except json.JSONDecodeError:
        return True, None


def render_error(message, status=422):
    return JsonResponse({'error_message': message}, status=status)


def valid_email(email):
    if email is None or email == '':
        return True, 'email cannot be empty'
    try:
        validate_email(email)
        return False, None
    except ValidationError:
        return True, 'email is incorrect'
