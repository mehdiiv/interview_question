from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from .models import User
from .common_methods import (
    create_jwt, fetch_data, render_error, valid_email,
    )


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
