from django.urls import path
from api.users import UsersView
from api.messages import MessagesViews

urlpatterns = [
    path('users/', UsersView.as_view(), name='users'),
    path('messages/', MessagesViews.as_view(), name='messages'),

]
