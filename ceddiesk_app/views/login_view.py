from rest_framework.views import APIView
from ceddiesk_app.apiresponse import ApiResponse
from rest_framework import status
from django.contrib.auth import authenticate, login
from ceddiesk_app.models import Teacher


class LoginView(APIView):
    """
    Handles logging users into the platform
    """

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
        login(request, user)
        if user is None:
            return ApiResponse(
                success=False,
                message='Incorrect nomina or password',
                data=None,
                status=status.HTTP_401_UNAUTHORIZED
            )
        teacher = Teacher.objects.get(user_id=user.id)
        return ApiResponse(
            success=True,
            message='Logged in',
            data=teacher,
            status=status.HTTP_200_OK
        )
