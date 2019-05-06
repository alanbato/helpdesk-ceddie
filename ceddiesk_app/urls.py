from django.urls import path

from . import views
from .views.login_view import LoginView
from .views.user_view import UserView
from .views.request_view import RequestView
from .views.adviser_view import AdviserView

urlpatterns = [
    # path('', views.index, name='index'),
    path(r'auth', UserView.as_view(), name='user'),
    path(r'adviser', AdviserView.as_view(), name='adviser'),
    path(r'auth/login', LoginView.as_view(), name='login'),
    path(r'request/(P<id>[0-9]+)', RequestView.as_view(), name='request'),
    path(r'request', RequestView.as_view(), name='request'),
]
