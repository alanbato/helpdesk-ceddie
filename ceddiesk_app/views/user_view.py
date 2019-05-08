from rest_framework.views import APIView
from rest_framework import status
from ceddiesk_app.apiresponse import ApiResponse
from django.contrib.auth.models import User
from ceddiesk_app.models import Teacher
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from ceddiesk_app.serializers import TeacherSerializer
from rest_framework.authtoken.models import Token


class UserView(APIView):
    """
    Handles user related requests:
        - Registration
        - User information
    """
    permission_classes = (AllowAny,)

    @csrf_exempt
    def post(self, request, format=None):
        """
        Register a user to the platform

        Expected request body:
        {
            'name': 'Juan Perez',
            'nomina': 'XXXXXXXX',
            'email': 'test@test.com',
            'password': '12345678'
        }

        :param request: The request data
        :param format: The request data format
        :return: A Response containing the registered user data
        """
        if not all(k in request.data for k in ('name', 'email', 'password', 'nomina')):
            return ApiResponse(
                success=False,
                message='Missing request parameters',
                data={
                    'error': 'Request call must include name, email, password and nomina'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(username=request.data['nomina']).exists():
            return ApiResponse(
                success=False,
                message='User with nomina already exists',
                data=None,
                status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.create_user(request.data['nomina'], request.data['email'], request.data['password'])
        if user:
            token = Token.objects.create(user_id=user.id)
            teacher = Teacher.objects.create(
                name=request.data['name'],
                email=request.data['email'],
                user_id=user.id,
                nomina=request.data['nomina']
            )
            if teacher:
                response = TeacherSerializer(teacher)
                response.data['token'] = token.key
                return ApiResponse(
                    success=True,
                    message='Teacher created successfully',
                    data={
                        'data': request.data,
                        'token': token.key
                    },
                    status=status.HTTP_201_CREATED
                )
        return ApiResponse(
            success=False,
            message='Error while creating user',
            data=None,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def get(self, request, format=None):
        """
        Gets a specified user by id

        No body, call to http://localhost:8000/user/<id>

        :param request: The request data
        :param format: The request data format
        :return: An ApiResponse containing the appropriate data
        """
        try:
            teacher = Teacher.objects.get(user_id=request.user.id)
            response = TeacherSerializer(teacher)
        except Teacher.DoesNotExist:
            return ApiResponse(
                success=False,
                message=f"Teacher with id: '{request.user.id}' not found",
                data=None,
                status=status.HTTP_404_NOT_FOUND
            )
        return ApiResponse(
            success=True,
            message='Teacher found',
            data=response.data,
            status=status.HTTP_200_OK
        )
