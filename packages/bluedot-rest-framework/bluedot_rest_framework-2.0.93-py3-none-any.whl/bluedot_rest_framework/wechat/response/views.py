from rest_framework.viewsets import ModelViewSet
from .models import WeChatResponseMaterial, WeChatResponseEvent
from .serializers import WeChatResponseMaterialSerializer, WeChatResponseEventSerializer


class WeChatResponseMaterialView(ModelViewSet):
    model_class = WeChatResponseMaterial
    serializer_class = WeChatResponseMaterialSerializer


class WeChatResponseEventView(ModelViewSet):
    model_class = WeChatResponseEvent
    serializer_class = WeChatResponseEventSerializer
