from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.func import orm_bulk_update
from bluedot_rest_framework.utils.jwt_token import jwt_create_token_wechat
from . import App
from .models import WeChatUser, WeChatUserOpenid

User = import_string('user.models')


class WeChatUserSet:
    appid = ''
    openid = ''

    def __init__(self, appid, user_info=None, openid=None):
        self.appid = appid
        if user_info or openid:
            if user_info:
                self.user_data = {
                    'unionid': user_info.get('unionid', ''),
                    'nick_name': user_info.get('nickname', ''),
                    'avatar_url': user_info.get('headimgurl', ''),
                    'gender': user_info.get('sex', ''),
                    'province': user_info.get('province', ''),
                    'city': user_info.get('city', ''),
                    'country': user_info.get('country', ''),
                    'language': user_info.get('language', '')
                }
                self.openid = user_info.get('openid', '')
            else:
                self.openid = openid
                user_info = App(self.appid).user.get(self.openid)
                self.__init__(appid=self.appid, user_info=user_info)
            self.wechat_user_queryset = WeChatUser.objects.filter(
                unionid=self.user_data['unionid']).first()
            self.handle_user()

    def create_user(self):
        self.wechat_user_queryset = WeChatUser.objects.create(**self.user_data)
        openid_data = {
            'wechat_id': self.wechat_user_queryset,
            'appid': self.appid,
            'openid': self.user_data['openid'],
            'subscribe': user['subscribe']
        }
        WeChatUserOpenid.objects.create(**openid_data)

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
        token = jwt_create_token_wechat(wechat_id=self.wechat_user_queryset.pk,
                                        unionid=self.wechat_user_queryset.unionid)
        return token

    def handle_subscribe(self, subscribe):
        self.wechat_user_queryset.subscribe = subscribe
        self.wechat_user_queryset.save()
