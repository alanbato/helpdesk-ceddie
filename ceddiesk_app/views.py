from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from ceddiesk_app.models import Adviser, Teacher, Request, Comment
from ceddiesk_app.serializers import (
    UserSerializer,
    GroupSerializer,
    AdviserSerializer,
    TeacherSerializer,
    RequestSerializer,
    CommentSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class AdviserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows advisers to be viewed or edited.
    """

    queryset = Adviser.objects.all()
    serializer_class = AdviserSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows teachers to be viewed or edited.
    """

    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class RequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows requests to be viewed or edited.
    """

    queryset = Request.objects.all().order_by("-date_created")
    serializer_class = RequestSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comments to be viewed or edited.
    """

    queryset = Comment.objects.all().order_by("-date_created")
    serializer_class = CommentSerializer
