from rest_framework.serializers import SerializerMethodField, CharField, IntegerField
from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.serializers import CustomSerializer


Configs = import_string('configs.models')


class ConfigsSerializer(CustomSerializer):

    class Meta:
        model = Configs
        fields = '__all__'
