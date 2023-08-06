from bluedot_rest_framework.utils.serializers import CustomSerializer
from .models import WeChatResponseMaterial, WeChatResponseEvent


class WeChatResponseMaterialSerializer(CustomSerializer):

    class Meta:
        model = WeChatResponseMaterial
        fields = '__all__'


class WeChatResponseEventSerializer(CustomSerializer):

    class Meta:
        model = WeChatResponseEvent
        fields = '__all__'
