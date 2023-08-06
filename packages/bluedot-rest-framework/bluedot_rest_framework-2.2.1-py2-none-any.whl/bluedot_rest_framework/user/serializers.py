from bluedot_rest_framework.utils.serializers import CustomSerializer
from rest_framework.serializers import SerializerMethodField
from bluedot_rest_framework import import_string

User = import_string('user.models')


class UserSerializer(CustomSerializer):

    class Meta:
        model = User
        fields = '__all__'
