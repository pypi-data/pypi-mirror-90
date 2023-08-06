from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.func import orm_bulk_update
from bluedot_rest_framework.utils.jwt_token import jwt_create_token_wechat
from . import OfficialAccount
from .models import WeChatUser

User = import_string('user.models')


class WeChatUserSet:

    def __init__(self, user_info=None, openid=None):
        if user_info or openid:
            if user_info:
                self.user_data = {
                    'unionid': user_info.get('unionid', ''),
                    'openid': user_info.get('openid', ''),
                    'nick_name': user_info.get('nickname', ''),
                    'avatar_url': user_info.get('headimgurl', ''),
                    'gender': user_info.get('sex', ''),
                    'province': user_info.get('province', ''),
                    'city': user_info.get('city', ''),
                    'country': user_info.get('country', ''),
                    'language': user_info.get('language', '')
                }
            else:
                user_info = OfficialAccount.user.get(openid)
                self.__init__(user_info=user_info)
            self.wechat_user_queryset = WeChatUser.objects.filter(
                openid=self.user_data['openid']).first()
            self.handle_user()

    def create_user(self):
        user = OfficialAccount.user.get(self.user_data['openid'])
        self.user_data['subscribe'] = user['subscribe']
        self.wechat_user_queryset = WeChatUser.objects.create(**self.user_data)

    def update_user(self):
        orm_bulk_update(self.wechat_user_queryset, self.user_data)

    def handle_user(self):
        if self.wechat_user_queryset:
            self.update_user()
        else:
            self.create_user()

    def get_token(self):
        user_id = 0
        user_queryset = User.objects.filter(
            wechat_id=self.wechat_user_queryset.pk).first()
        if user_queryset:
            user_id = user_queryset.pk
        token = jwt_create_token_wechat(
            openid=self.wechat_user_queryset.openid, unionid=self.wechat_user_queryset.unionid, userid=user_id, wechat_id=self.wechat_user_queryset.pk)
        return token

    def handle_subscribe(self, subscribe):
        self.wechat_user_queryset.subscribe = subscribe
        self.wechat_user_queryset.save()
