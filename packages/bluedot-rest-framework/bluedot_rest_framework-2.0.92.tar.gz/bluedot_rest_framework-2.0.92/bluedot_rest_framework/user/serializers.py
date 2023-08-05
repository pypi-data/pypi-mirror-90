from bluedot_rest_framework.utils.serializers import CustomSerializer
from rest_framework.serializers import SerializerMethodField
from bluedot_rest_framework import import_string
from bluedot_rest_framework.wechat.models import WeChatUser
from bluedot_rest_framework.wechat.serializers import WeChatUserSerializer

User = import_string('USER.models')


class UserSerializer(CustomSerializer):
    wechat_profile = SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_wechat_profile(self, queryset):
        wechat_queryset = WeChatUser.objects.filter(
            pk=queryset.wechat_id).first()
        serializer = WeChatUserSerializer(wechat_queryset)
        return serializer.data
