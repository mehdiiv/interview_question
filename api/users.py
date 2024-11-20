from django.views import View
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
import json
from .models import User
from .common_methods import create_jwt


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


@method_decorator(csrf_exempt, name='dispatch')
class UsersView(View):
    def post(self, request):
        error, load_data = fetch_data(request.body)
        if error:
            return render_error('invalid json')
        error, error_message = valid_email(load_data.get('email'))
        if error:
            return render_error(error_message)
        if User.objects.filter(email=load_data.get('email')).exists():
            return render_error('email alredy exist'
                                )
        user = User.objects.create(email=load_data['email'],
                                   json_web_token=create_jwt(load_data['email'
                                                                       ]))
        return JsonResponse(model_to_dict(user), status=201)

    def get(self, request):
        limit, offset = self.set_limit_offset(request)
        users = User.objects.all()[offset:offset+limit]
        users_list = []
        for item in users:
            users_list.append(model_to_dict(item))
        return JsonResponse({'users': users_list}, status=200)

    def set_limit_offset(self, request):
        offset = 0
        limit = 10
        if request.GET.get('limit') and request.GET.get(
            'offset') is not None and request.GET.get(
                'limit').isdigit() and request.GET.get(
                    'offset').isdigit():
            offset = int(request.GET.get('offset'))
            limit = int(request.GET.get('limit'))
            if limit > 30:
                limit = 30
        return limit, offset
