from django.urls import path

from . import views
from .views.login_view import LoginView
from .views.user_view import UserView
from .views.request_view import RequestView

urlpatterns = [
    # path('', views.index, name='index'),
    path(r'auth', UserView.as_view(), name='user'),
    # path(r'auth', UserView.as_view(), name='user'),
    path(r'auth/login', LoginView.as_view(), name='login'),
    path(r'request/(?P<id>\d+)/$', UserView.as_view(), name='request'),
]
