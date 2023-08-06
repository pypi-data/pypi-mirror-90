from django_filters import rest_framework as filters
from .models import EventSchedule


class EventScheduleFilter(filters.FilterSet):
    topic_title = filters.CharFilter(
        field_name='topic_title', lookup_expr='contains')
    event_id = filters.NumberFilter(
        field_name='event_id', lookup_expr='exact')

    class Meta:
        model = EventSchedule
        fields = ['topic_title', 'event_id']
