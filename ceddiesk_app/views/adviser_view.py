from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView

from ceddiesk_app.apiresponse import ApiResponse
from ceddiesk_app.models import Adviser
from ceddiesk_app.serializers import AdviserSerializer
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt


class AdviserView(APIView):
    """
    Handles creation and managing of advisers
    """
    permission_classes = (AllowAny,)

    @csrf_exempt
    def post(self, request, format=None):
        """
        Creates an adviser. For now this is an unauthenticated call.
        :param request: The request data
        :param format: The request data format
        :return: An ApiResponse
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
            adviser = Adviser.objects.create(
                name=request.data['name'],
                email=request.data['email'],
                user_id=user.id,
                nomina=request.data['nomina']
            )
            if adviser:
                response = AdviserSerializer(adviser)
                return ApiResponse(
                    success=True,
                    message='Adviser created successfully',
                    data=response.data,
                    status=status.HTTP_201_CREATED
                )
        return ApiResponse(
            success=False,
            message='Error while creating user',
            data=None,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
