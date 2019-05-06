from rest_framework.views import APIView
from ceddiesk_app.apiresponse import ApiResponse
from rest_framework import status
from ceddiesk_app.models import Request


class RequestView(APIView):
    """
    Handles all request related calls.
    """

    def post(self, request, format=None):
        """
        Creates a new request with the specified data.

        Example request body:
        {
            'course_name': 'Compiladores',
            'course_id': 'TC2001',
            'request_type': 'PLAT',
            'platform_type': 'BLACK',
            'advice_type': 'EMA',
            'description': 'Es que no jala'
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
                'advise_type',
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
        req = Request.objects.create(request=request.data)
        if req is not None:
            return ApiResponse(
                success=True,
                message='Request created successfully',
                data=req,
                status=status.HTTP_201_CREATED
            )
        return ApiResponse(
            success=False,
            message='An error occurred while creating the request',
            data=None,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def get(self, request, id, format=None):
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
        if id is not None:
            try:
                req = Request.objects.get(id=id)
                return ApiResponse(
                    success=True,
                    message='Request found',
                    data=req,
                    status=status.HTTP_200_OK
                )
            except Request.DoesNotExist:
                return ApiResponse(
                    success=False,
                    message=f"Request with id: '{id}' not found",
                    data=None,
                    status=status.HTTP_404_NOT_FOUND
                )
        reqs = Request.objects.filter(teacher__user_id=request.user.id)
        return ApiResponse(
            success=True,
            message='Requests found',
            data=reqs,
            status=status.HTTP_200_OK
        )

    def delete(self, request, id, format=None):
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
        if not request.user.is_admin:
            return ApiResponse(
                success=False,
                message='Unauthorized user',
                data={
                    'error': 'User must be admin to delete requests'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
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
        if not request.user.is_admin:
            return ApiResponse(
                success=False,
                message='Unauthorized user',
                data={
                    'error': 'User must be admin to delete requests'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        req = Request.objects.update(request.data)
        if req:
            return ApiResponse(
                success=True,
                message='Request updated',
                data=req,
                status=status.HTTP_200_OK
            )
        return ApiResponse(
            success=False,
            message='An error occurred while updating the request',
            data=None,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
