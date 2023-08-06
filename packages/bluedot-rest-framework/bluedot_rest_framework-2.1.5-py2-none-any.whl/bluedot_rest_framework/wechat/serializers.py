from rest_framework.serializers import SerializerMethodField
from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.serializers import CustomSerializer

from bluedot_rest_framework.wechat.models import WeChatUser, WeChatUserOpenid

User = import_string('user.models')
UserSerializer = import_string('user.serializers')


class WeChatUserSerializer(CustomSerializer):
    profile = SerializerMethodField()
    openid = SerializerMethodField()

    class Meta:
        model = WeChatUser
        fields = '__all__'

    def get_profile(self, queryset):
        user_queryset = User.objects.filter(
            wechat_id=queryset.pk).first()
        if user_queryset:
            serializer = UserSerializer(user_queryset)
            return serializer.data
        else:
            return None

    def get_openid(self, queryset):
        openid_queryset = queryset.wechat_set.all()
        serializer = WeChatUserOpenidSerializer(openid_queryset)
        return serializer.data


class WeChatUserOpenidSerializer(CustomSerializer):
    class Meta:
        model = WeChatUserOpenid
        fields = '__all__'
