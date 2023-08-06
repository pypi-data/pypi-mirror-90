import requests
from django.conf import settings
from django.core.mail.message import EmailMessage
from django.core.mail import send_mail
from rest_framework.decorators import action
from rest_framework.response import Response
from bluedot_rest_framework.wechat import OfficialAccount
from bluedot_rest_framework.utils.oss import OSS
from bluedot_rest_framework.utils.crypto import AESEncrypt
from bluedot_rest_framework.utils.jwt_token import jwt_get_userid_handler, jwt_get_userinfo_handler, jwt_get_openid_handler
from datetime import datetime
from .register.models import EventRegister
from .data_download.models import EventDataDownload


class FrontendView:

    @action(detail=False, methods=['post'], url_path='list-frontend', url_name='list-frontend')
    def list_frontend(self, request, *args, **kwargs):
        user_id = jwt_get_userid_handler(request.auth)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            data = self.get_serializer(page, many=True).data

            for item in data['data']:
                item['is_register'] = 0
                if EventRegister.objects.filter(
                        user_id=user_id, event_id=data['event_id']):
                    item['is_register'] = 1

            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='countdown', url_name='countdown')
    def countdown(self, request, *args, **kwargs):
        _id = request.query_params.get('id', '')
        queryset = self.model_class.objects.get(pk=_id)
        now_time = datetime.now()
        seconds = (queryset.start_time - now_time).total_seconds()
        return Response({'seconds': seconds})

    @action(detail=False, methods=['get'], url_path='share-qrcode-officialaccount', url_name='share-qrcode-officialaccount')
    def share_qrcode_officialaccount(self, request, *args, **kwargs):
        _id = request.query_params.get('id', '')
        openid = jwt_get_openid_handler(request.auth)
        scene_str = f'bluedot_event_share_id_{_id}_openid_{openid}'
        result = OfficialAccount.qrcode.create({
            # 'expire_seconds': 86400,
            'action_name': 'QR_LIMIT_SCENE',
            'action_info': {
                'scene': {'scene_str': scene_str},
            }
        })
        res = OfficialAccount.qrcode.get_url(result['ticket'])
        path = f"event/qrcode-official-account/{scene_str}.jpg"
        OSS.put_object_internet(res, path)
        url = f"https://{settings.BLUEDOT_REST_FRAMEWORK['UTILS']['OSS']['bucket_name']}.oss-cn-beijing.aliyuncs.com/{path}"
        return Response({'url': url})

    # @action(detail=False, methods=['get'], url_path='share-qrcode-miniprogram', url_name='share-qrcode-miniprogram')
    # def share_qrcode_official_account(self, request, *args, **kwargs):
    #     _id = request.query_params.get('id', '')
    #     queryset = self.model_class.objects.get(pk=_id)
    #     now_time = datetime.now()
    #     seconds = (queryset.start_time - now_time).total_seconds()
    #     return Response({'seconds': seconds})
