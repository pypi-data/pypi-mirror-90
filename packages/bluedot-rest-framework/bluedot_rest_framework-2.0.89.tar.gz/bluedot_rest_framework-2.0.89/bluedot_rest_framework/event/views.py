
from datetime import datetime
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, AllView
from bluedot_rest_framework.utils.jwt_token import jwt_get_userid_handler
from bluedot_rest_framework.utils.func import get_tree
from bluedot_rest_framework.utils.area import area
from .live.views import LiveView
from .frontend_views import FrontendView

Event = import_string('EVENT.models')
EventSerializer = import_string('EVENT.serializers')
EventRegister = import_string('EVENT.register.models')


class EventView(CustomModelViewSet, FrontendView, LiveView, AllView):
    model_class = Event
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filterset_fields = {
        'event_type': {
            'field_type': 'int',
            'lookup_expr': ''
        },
        'time_state': {
            'start_time': 'start_time',
            'end_time': 'end_time'
        },
        'title': {
            'field_type': 'string',
            'lookup_expr': '__icontains'
        }
    }

    @action(detail=False, methods=['get'], url_path='area', url_name='area')
    def area(self, request, *args, **kwargs):
        return Response(area)
