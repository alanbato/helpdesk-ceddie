from django.contrib.auth.models import User, Group
from rest_framework import serializers

from ceddiesk_app.models import Adviser, Teacher, Request, Comment


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        """ Creates and returns a new user """
        password = validated_data.pop("password")
        # Validating Data
        user = User.objects.create_user(username=validated_data["username"])

        user.set_password(password)
        user.save()

        return user


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class AdviserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Adviser
        depth = 1
        fields = ('user_id', 'name', 'nomina', 'email')

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(user_data["username"])
        user.set_password(user_data["password"])
        adviser = Adviser.objects.create(user=user, **validated_data)
        adviser.save()
        return adviser


class TeacherSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    
    class Meta:
        model = Teacher
        depth = 1
        fields = ('user_id', 'name', 'nomina', 'email')

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(user_data["username"])
        user.set_password(user_data["password"])
        teacher = Teacher.objects.create(user=user, **validated_data)
        teacher.save()
        return teacher


class RequestSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()

    class Meta:
        model = Request
        depth = 1
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user', 'request', 'text')