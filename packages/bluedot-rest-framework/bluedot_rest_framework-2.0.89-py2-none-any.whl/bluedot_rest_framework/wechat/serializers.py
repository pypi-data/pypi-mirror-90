from bluedot_rest_framework.utils.serializers import CustomSerializer

from bluedot_rest_framework.wechat.models import WeChatUser


class WeChatUserSerializer(CustomSerializer):

    class Meta:
        model = WeChatUser
        fields = '__all__'
