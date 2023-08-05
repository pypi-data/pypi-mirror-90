import json
from websocket import create_connection
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from bluedot_rest_framework.utils.oss import OSS
from bluedot_rest_framework.wechat import OfficialAccount
from bluedot_rest_framework.wechat.utils import create_auth_token
from bluedot_rest_framework import import_string

from .models import WeChatLogin

User = import_string('USER.models')


class WeChatLoginView(APIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        scene_str = request.query_params.get('code', '')
        result = OfficialAccount.qrcode.create({
            'expire_seconds': 86400,
            'action_name': 'QR_STR_SCENE',
            'action_info': {
                'scene': {'scene_str': scene_str},
            }
        })
        WeChatLogin.objects.create(scene_str=scene_str)
        return Response(result)


class WeChatLoginWebSocketView(APIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        scene_str = request.query_params.get('scene_str', '')
        openid = request.query_params.get('openid', '')
        user_info = OfficialAccount.user.get(openid)
        token = create_auth_token(user_info)
        ws = create_connection(
            "ws://cpa-global-wechat.bluewebonline.com/ws/wechat/login/" + scene_str)
        ws.send(json.dumps({'token': token}))
        ws.close()
        return Response({'token': token})
