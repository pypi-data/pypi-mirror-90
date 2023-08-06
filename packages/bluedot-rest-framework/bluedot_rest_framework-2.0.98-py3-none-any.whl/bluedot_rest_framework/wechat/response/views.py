from bluedot_rest_framework.utils.viewsets import CustomModelViewSet
from .models import WeChatResponseMaterial, WeChatResponseEvent
from .serializers import WeChatResponseMaterialSerializer, WeChatResponseEventSerializer


class WeChatResponseMaterialView(CustomModelViewSet):
    model_class = WeChatResponseMaterial
    serializer_class = WeChatResponseMaterialSerializer


class WeChatResponseEventView(CustomModelViewSet):
    model_class = WeChatResponseEvent
    serializer_class = WeChatResponseEventSerializer
