from django.db.models import Q
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from .models import Message
from .common_methods import (
    render_error, fetch_data,
    authorization, AuthorizeError,
    set_limit_offset,
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

    def get(self, request):
        try:
            user = authorization(request.headers.get('Authorization'))
            messges = Message.objects.filter(user=user)
            if request.GET.get('search_by') is not None:
                search_by = request.GET.get('search_by')
                messges = Message.objects.filter(
                    Q(body__icontains=search_by), user=user
                )
            limit, offset = set_limit_offset(request)
            messges = messges[offset:offset+limit]
            messages_list = []
            for item in messges:
                messages_list.append(model_to_dict(item))
            return JsonResponse({'messages': messages_list}, status=200)
        except AuthorizeError:
            return render_error('you are not authorised')


@method_decorator(csrf_exempt, name='dispatch')
class MessageView(View):
    def get(self, request, pk):
        try:
            user = authorization(request.headers.get('Authorization'))
            message = Message.objects.filter(user=user, id=pk)
            if not message.exists():
                return render_error('message does not exist')
            message_list = []
            for item in message:
                message_list.append(model_to_dict(item))
            return JsonResponse({'message': message_list}, status=200)
        except AuthorizeError:
            return render_error('you are not authorised')
