from bluedot_rest_framework.utils.serializers import CustomSerializer
from .models import WeChatQrcode, WeChatQrcodeLogin


class WeChatQrcodeSerializer(CustomSerializer):

    class Meta:
        model = WeChatQrcode
        fields = '__all__'


class WeChatQrcodeloginSerializer(CustomSerializer):

    class Meta:
        model = WeChatQrcodeLogin
        fields = '__all__'
