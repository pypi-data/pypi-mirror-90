from django_filters import rest_framework as filters
from .models import Event
from datetime import datetime


class EventFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='contains')
    event_type = filters.NumberFilter(
        field_name='event_type', lookup_expr='exact')
    time_state = filters.NumberFilter(method='time_state_filter')

    class Meta:
        model = Event
        fields = ['title', 'event_type']

    def time_state_filter(self, queryset, name, value):
        date_now = datetime.now()
        filters = {}
        if value == 1:
            filters['start_time__gt'] = date_now
        elif value == 2:
            filters['start_time__lt'] = date_now
            filters['end_time__gt'] = date_now
        elif value == 3:
            filters['end_time__lt'] = date_now
        return queryset.filter(**filters)
