from django_filters import rest_framework as filters
from .models import EventComment


class EventCommentFilter(filters.FilterSet):
    state = filters.NumberFilter(
        field_name='state', lookup_expr='exact')
    schedule_id = filters.NumberFilter(
        field_name='schedule_id', lookup_expr='exact')
    event_id = filters.NumberFilter(
        field_name='event_id', lookup_expr='exact')

    class Meta:
        model = EventComment
        fields = ['state', 'schedule_id', 'event_id']
