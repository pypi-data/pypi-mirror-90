from functools import wraps

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


def api(req_model=None,
        res_model=None,
        permissions=tuple(),
        methods=('post',),
        renderers=(JSONRenderer,)):
    def decorator(func):
        @wraps(func)
        @swagger_auto_schema(methods=methods, query_serializer=req_model)
        @api_view(methods)
        @renderer_classes(renderers)
        @permission_classes(permissions)
        def decorated(request):
            args = []
            request_data = request.data
            if func.__code__.co_argcount:
                if req_model:
                    serializer_data = req_model(data=request.data)
                    serializer_data.is_valid(raise_exception=True)
                    request_data = serializer_data.data
                args = [request_data]
            response_data = func(*args)
            return Response(res_model(response_data).data)

        return decorated

    return decorator
