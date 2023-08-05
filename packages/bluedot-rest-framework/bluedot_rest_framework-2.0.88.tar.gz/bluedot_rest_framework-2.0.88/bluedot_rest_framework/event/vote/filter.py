from django_filters import rest_framework as filters
from .models import EventVote


class EventVoteFilter(filters.FilterSet):
    title = filters.CharFilter(
        field_name='title', lookup_expr='contains')
    event_id = filters.NumberFilter(
        field_name='event_id', lookup_expr='exact')
    schedule_id = filters.NumberFilter(
        field_name='schedule_id', lookup_expr='exact')

    class Meta:
        model = EventVote
        fields = ['title', 'event_id', 'schedule_id']
