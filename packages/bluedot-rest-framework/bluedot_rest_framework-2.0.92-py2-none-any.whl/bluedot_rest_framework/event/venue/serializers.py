from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.serializers import CustomSerializer


EventVenue = import_string('EVENT.venue.models')


class EventVenueSerializer(CustomSerializer):

    class Meta:
        model = EventVenue
        fields = '__all__'
