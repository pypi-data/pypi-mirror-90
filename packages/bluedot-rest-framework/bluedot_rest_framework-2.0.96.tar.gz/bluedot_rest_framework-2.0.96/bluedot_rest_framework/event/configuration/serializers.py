from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.serializers import CustomSerializer

EventConfiguration = import_string('EVENT.configuration.models')


class EventConfigurationSerializer(CustomSerializer):

    class Meta:
        model = EventConfiguration
        fields = '__all__'
