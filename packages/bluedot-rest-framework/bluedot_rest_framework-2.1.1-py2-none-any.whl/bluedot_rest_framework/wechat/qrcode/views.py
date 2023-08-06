from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from bluedot_rest_framework.utils.viewsets import CustomModelViewSet
from bluedot_rest_framework.utils.jwt_token import jwt_create_token_wechat
from . import CreateQrcode
from .models import WeChatQrcode, WeChatQrcodeLogin
from .serializers import WeChatQrcodeSerializer
from bluedot_rest_framework.user.models import User


class WeChatQrcodeView(CustomModelViewSet):
    model_class = WeChatQrcode
    serializer_class = WeChatQrcodeSerializer

    @action(detail=False, methods=['post'], url_path='miniprogram', url_name='miniprogram')
    def miniprogram(self, request, *args, **kwargs):
        user_name = 'gh_5645640b48e2'
        page = request.data.get('page', None)
        param = request.data.get('param', None)

        data = WeChatQrcode.objects.filter(
            param=param).first()

        if data is None:
            qrcode = WeChatQrcode(
                user_name=user_name, param=param)
            qrcode.save()

            _id = str(qrcode.id)
            url = CreateQrcode.miniprogram(_id, page)

            qrcode.url = url
            qrcode.save()
        else:
            url = data.url

        return Response({'url': url})

    @action(detail=False, methods=['get'], url_path='offiaccount_event_live', url_name='offiaccount_event_live')
    def offiaccount_event_live(self, request, *args, **kwargs):
        event_id = request.query_params.get('event_id')
        scene_str = f"event_{event_id}"
        url = CreateQrcode.offiaccount_event_live(scene_str)
        return Response({'url': url})


class WeChatQrcodeLoginView(APIView):

    permission_classes = []

    def get(self, request, *args, **kwargs):
        code = request.query_params.get('code', None)
        queryset = WeChatQrcodeLogin.objects.filter(code=code).first()
        token = ''
        if queryset:
            user_queryset = User.objects.filter(unionid=queryset.unionid).order_by(
                '-created').first()
            if user_queryset:
                token = jwt_create_token_wechat(
                    openid=user_queryset.openid, unionid=user_queryset.unionid, userid=user_queryset.pk, wechat_id=queryset.wechat_id)

        return Response({'code': code, 'token': token})

    def post(self, request, *args, **kwargs):
        code = request.data.get('code', None)
        scene_str = f"cpa_pc_login_{code}"
        url = CreateQrcode.offiaccount_event_pc(scene_str)
        WeChatQrcodeLogin.objects.create(code=code, url=url)
        return Response({'url': url})
