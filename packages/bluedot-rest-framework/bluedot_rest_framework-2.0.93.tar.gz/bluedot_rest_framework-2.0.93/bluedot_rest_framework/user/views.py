from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, user_perform_create, AllView
from bluedot_rest_framework.utils.jwt_token import jwt_create_token_wechat, jwt_get_userinfo_handler
from .frontend_views import FrontendView


User = import_string('USER.models')
UserSerializer = import_string('USER.serializers')


class UserView(CustomModelViewSet, FrontendView):
    model_class = User
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user_id, openid, unionid, wechat_id = jwt_get_userinfo_handler(
            self.request.auth)
        serializer.save(openid=openid, unionid=unionid, wechat_id=wechat_id)
        user_data = serializer.data
        user_data['token'] = jwt_create_token_wechat(
            openid=user_data['openid'], unionid=user_data['unionid'], userid=user_data['id'], wechat_id=user_data['wechat_id'])
        return Response(user_data, status=status.HTTP_201_CREATED)
