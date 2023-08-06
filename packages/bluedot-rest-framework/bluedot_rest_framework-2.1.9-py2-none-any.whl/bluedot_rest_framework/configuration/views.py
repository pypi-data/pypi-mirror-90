from rest_framework.permissions import IsAuthenticatedOrReadOnly

from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet


Configuration = import_string('configuration.models')
ConfigurationSerializer = import_string('configuration.serializers')


class ConfigurationView(CustomModelViewSet):
    model_class = Configuration
    serializer_class = ConfigurationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
