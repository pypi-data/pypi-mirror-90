from rest_framework.permissions import IsAuthenticatedOrReadOnly

from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet


Configs = import_string('configs.models')
ConfigsSerializer = import_string('configs.serializers')


class ConfigsView(CustomModelViewSet):
    model_class = Configs
    serializer_class = ConfigsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
