from rest_framework.decorators import action
from rest_framework.response import Response
from bluedot_rest_framework.utils.jwt_token import jwt_get_userid_handler


class FrontendView:

    @action(detail=False, methods=['get'], url_path='current', url_name='current')
    def current(self, request, *args, **kwargs):
        user_id = jwt_get_userid_handler(request.auth)
        queryset = self.model_class.objects.filter(pk=user_id).first()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
