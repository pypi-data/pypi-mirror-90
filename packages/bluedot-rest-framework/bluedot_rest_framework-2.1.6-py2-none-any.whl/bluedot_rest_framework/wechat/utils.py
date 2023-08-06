from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.func import orm_bulk_update
from bluedot_rest_framework.utils.jwt_token import jwt_create_token_wechat
from .models import WeChatUser
User = import_string('USER.models')


def create_auth_token(user_info):
    user_data = {
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

    wechat_queryset = WeChatUser.objects.filter(
        openid=user_info['openid']).first()
    if wechat_queryset:
        orm_bulk_update(wechat_queryset, user_data)
    else:
        wechat_queryset = WeChatUser.objects.create(**user_data)
    user_id = 0
    user_queryset = User.objects.filter(
        wechat_id=wechat_queryset.pk).first()
    if user_queryset:
        user_id = user_queryset.pk
    token = jwt_create_token_wechat(
        openid=wechat_queryset.openid, unionid=wechat_queryset.unionid, userid=user_id, wechat_id=wechat_queryset.pk)
    return token
