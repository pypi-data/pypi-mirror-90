from bluedot_rest_framework.wechat import OfficialAccount
from rest_framework.views import APIView
from django.http import HttpResponse
from .models import WeChatQrcode
from rest_framework.response import Response


class WeChatQrcodeView(APIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        scene_str = self.request.data.get('scene_str', None)
        result = OfficialAccount.qrcode.create({
            'action_name': 'QR_LIMIT_STR_SCENE',
            'action_info': {
                'scene': {'scene_str': scene_str},
            }
        })
        WeChatQrcode.objects.create(scene_str=scene_str)
        return Response(result)
