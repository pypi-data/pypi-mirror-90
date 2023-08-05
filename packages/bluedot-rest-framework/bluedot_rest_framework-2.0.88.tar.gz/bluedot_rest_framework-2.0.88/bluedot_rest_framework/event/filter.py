from django_filters import rest_framework as filters
from .models import Event


class EventFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='contains')
    event_type = filters.NumberFilter(
        field_name='event_type', lookup_expr='exact')

    class Meta:
        model = Event
        fields = ['title', 'event_type']
