from rest_framework.views import APIView
from ceddiesk_app.apiresponse import ApiResponse
from rest_framework import status
from ceddiesk_app.models import Request, Teacher, Adviser
from ceddiesk_app.serializers import RequestSerializer


class RequestView(APIView):
    """
    Handles all request related calls.
    """

    def post(self, request, format=None):
        """
        Creates a new request with the specified data.

        Example request body:
        {
            "course_name": "Compiladores",
            "course_id": "TC2001",
            "request_type": "PLAT",
            "platform_type": "BLACK",
            "advice_type": "EMA",
            "description": "Es que no jala"
        }

        :param request: The request data
        :param format: The request format
        :return: An ApiResponse with the appropriate response
        """
        if not request.user.is_authenticated:
            return ApiResponse(
                success=False,
                message='Unauthorized user',
                data={
                    'error': 'User must be authenticated to access the resource'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        if not all(k in request.data for k in (
                'course_name',
                'course_id',
                'request_type',
                'platform_type',
                'advice_type',
                'description'
        )):
            return ApiResponse(
                success=False,
                message='Missing request parameters',
                data={
                    'error': 'Request parameters must include course_name, course_id, request_type, advice_type, '
                             'platform_type and description '
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        teacher = Teacher.objects.get(user_id=request.user.id)
        req = Request.objects.create(
            course_name=request.data['course_name'],
            course_id=request.data['course_id'],
            request_type=request.data['request_type'],
            platform_type=request.data['platform_type'],
            advice_type=request.data['advice_type'],
            description=request.data['description'],
            teacher_id=teacher.id
        )
        if req is not None:
            response = RequestSerializer(req)
            return ApiResponse(
                success=True,
                message='Request created successfully',
                data=response.data,
                status=status.HTTP_201_CREATED
            )
        return ApiResponse(
            success=False,
            message='An error occurred while creating the request',
            data=None,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def get(self, request, format=None):
        """
        Returns all requests if no id is specified, returns the specified request detail otherwise
        :param id: The id of the request to get, can be unspecified
        :param request: The request data
        :param format: The request data format
        :return: An ApiResponse with the appropriate response
        """
        if not request.user.is_authenticated:
            return ApiResponse(
                success=False,
                message='Unauthorized user',
                data={
                    'error': 'User must be authenticated to access the resource'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        id = request.query_params.get('id', None)
        if id:
            try:
                req = Request.objects.get(id=id)
                response = RequestSerializer(req)
                return ApiResponse(
                    success=True,
                    message='Request found',
                    data=response.data,
                    status=status.HTTP_200_OK
                )
            except Request.DoesNotExist:
                return ApiResponse(
                    success=False,
                    message=f"Request with id: '{id}' not found",
                    data=None,
                    status=status.HTTP_404_NOT_FOUND
                )
        if Adviser.objects.filter(user_id=request.user.id).exists():
            reqs = Request.objects.all()
        else:
            reqs = Request.objects.filter(teacher__user_id=request.user.id)
        response = RequestSerializer(reqs, many=True)
        return ApiResponse(
            success=True,
            message='Requests found',
            data=response.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, format=None):
        """
        Deletes the specified request. Can only be called by admin users.
        :param id: The id of the request to delete
        :param request: The request data
        :param format: The request data format
        :return: An ApiResponse with the appropriate response
        """
        if not request.user.is_authenticated:
            return ApiResponse(
                success=False,
                message='Unauthorized user',
                data={
                    'error': 'User must be authenticated to access the resource'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        if not Adviser.objects.filter(user_id=request.user.id).exists():
            return ApiResponse(
                success=False,
                message='Unauthorized user',
                data={
                    'error': 'User must be adviser to delete requests'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        id = request.query_params.get('id', None)
        req = Request.objects.get(id=id)
        req.delete()
        return ApiResponse(
            success=True,
            message=f'Request {id} deleted',
            data=None,
            status=status.HTTP_200_OK
        )

    def put(self, request, format=None):
        """
        Updates a specific request identified by the id
        :param request: The request data
        :param format: The request data format
        :return: An ApiResponse with the appropriate response
        """
        if not request.user.is_authenticated:
            return ApiResponse(
                success=False,
                message='Unauthorized user',
                data={
                    'error': 'User must be authenticated to access the resource'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        if not Adviser.objects.filter(user_id=request.user.id).exists():
            return ApiResponse(
                success=False,
                message='Unauthorized user',
                data={
                    'error': 'User must be admin to delete requests'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        req = Request.objects.get(id=request.data['id'])
        for k in request.data:
            if request.data[k] is not None:
                req.__setattr__(k, request.data[k])
        req.save()
        response = RequestSerializer(req)
        if req:
            return ApiResponse(
                success=True,
                message='Request updated',
                data=response.data,
                status=status.HTTP_200_OK
            )
        return ApiResponse(
            success=False,
            message='An error occurred while updating the request',
            data=None,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
