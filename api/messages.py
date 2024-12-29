from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from .models import Message
from .common_methods import (
    render_error, fetch_data,
    authorization, AuthorizeError,
 )


@method_decorator(csrf_exempt, name='dispatch')
class MessagesViews(View):
    def post(self, request):
        try:
            user = authorization(request.headers.get('Authorization'))
            error, message_load_data = fetch_data(request.body)
            if error:
                return render_error('invalid json')
            if message_load_data.get(
                'title'
            ) == '' or message_load_data.get('title') is None:
                return render_error('title cannot be empty')
            elif Message.objects.filter(
                title=message_load_data['title'], user=user
            ).exists():
                return render_error('this title have been exist')
            message = Message.objects.create(
                user=user, title=message_load_data[
                    'title'
                ], body=message_load_data['body']
            )
            return JsonResponse(model_to_dict(message), status=201)
        except AuthorizeError:
            return render_error('you are not authorised')
