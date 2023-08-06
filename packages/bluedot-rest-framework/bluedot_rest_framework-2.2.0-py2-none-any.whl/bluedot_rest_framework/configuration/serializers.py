from rest_framework.serializers import SerializerMethodField, CharField, IntegerField
from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.serializers import CustomSerializer


Configuration = import_string('configuration.models')


class ConfigurationSerializer(CustomSerializer):

    class Meta:
        model = Configuration
        fields = '__all__'
