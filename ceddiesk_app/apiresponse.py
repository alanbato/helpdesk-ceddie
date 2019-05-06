from rest_framework.response import Response


class ApiResponse(Response):
    def __init__(self, success=True, message="", data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        super(ApiResponse, self).__init__(dict(success=success, message=message, data=data), status, template_name,
                                          headers, exception, content_type)
