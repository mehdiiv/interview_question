from django.urls import path
from api.users import UsersView

urlpatterns = [
    path('users/', UsersView.as_view(), name='users'),
]
