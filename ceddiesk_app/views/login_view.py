from rest_framework.views import APIView
from ceddiesk_app.apiresponse import ApiResponse
from rest_framework import status
from django.contrib.auth import authenticate, login
from ceddiesk_app.models import Teacher, Adviser
from ceddiesk_app.serializers import TeacherSerializer, AdviserSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token


class LoginView(APIView):
    """
    Handles logging users into the platform
    """
    permission_classes = (AllowAny,)

    @csrf_exempt
    def post(self, request, format=None):
        """
        Logs a user into the platform given their username and password

        Example request body:
        {
            'username': 'XXXXXXXX',
            'password': '12345678'
        }

        :param request: The request data
        :param format: The request format
        :return: An ApiResponse with the appropriate response
        """
        if not all(k in request.data for k in ('nomina', 'password')):
            return ApiResponse(
                success=False,
                message='Missing request parameters',
                data={
                    'error': 'Request parameters must include username and password'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(request, username=request.data['nomina'], password=request.data['password'])
        if user is None:
            return ApiResponse(
                success=False,
                message='Incorrect nomina or password',
                data=None,
                status=status.HTTP_401_UNAUTHORIZED
            )
        login(request, user)
        try:
            teacher = Teacher.objects.get(user_id=user.id)
            response = TeacherSerializer(teacher)
        except Teacher.DoesNotExist:
            adviser = Adviser.objects.get(user_id=user.id)
            response = AdviserSerializer(adviser)
        token = Token.objects.create(user_id=user.id)
        return ApiResponse(
            success=True,
            message='Logged in',
            data={
                'data': response.data,
                'token': token.key
            },
            status=status.HTTP_200_OK
        )
