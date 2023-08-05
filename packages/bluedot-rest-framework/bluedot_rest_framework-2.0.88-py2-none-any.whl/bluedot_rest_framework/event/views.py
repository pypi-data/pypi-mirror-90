
from datetime import datetime
from rest_framework.decorators import action
from rest_framework.response import Response
from bluedot_rest_framework import import_string
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, AllView
from bluedot_rest_framework.utils.jwt_token import jwt_get_userid_handler
from bluedot_rest_framework.utils.func import get_tree
from bluedot_rest_framework.utils.area import area
from .live.views import LiveView
from .frontend_views import FrontendView
from .filter import EventFilter
from rest_framework import filters
from datetime import datetime
from rest_framework import status
from django_filters.rest_framework.backends import DjangoFilterBackend

Event = import_string('EVENT.models')
EventSerializer = import_string('EVENT.serializers')
EventRegister = import_string('EVENT.register.models')


class EventView(CustomModelViewSet, FrontendView, LiveView, AllView):
    model_class = Event
    serializer_class = EventSerializer
    filterset_class = EventFilter
    filter_backends = [
        DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = '__all__'
    permission_classes = [IsAuthenticatedOrReadOnly]

    @ action(detail=False, methods=['get'], url_path='area', url_name='area')
    def area(self, request, *args, **kwargs):
        return Response(area)

    # @ action(detail=False, methods=['get'], url_path='state', url_name='state')
    # def state(self, request, *args, **kwargs):
    #     time_state = request.query_params.get('time_state', None)
    #     ordering = request.query_params.get('ordering', None)
    #     now_time = datetime.now()
    #     filters = {}
    #     if time_state == '1':
    #         filters['start_time__gt'] = now_time
    #     elif time_state == '2':
    #         filters['start_time__lt'] = now_time
    #         filters['end_time__gt'] = now_time
    #     elif time_state == '3':
    #         filters['end_time__lt'] = now_time
    #     event_queryset = self.model_class.objects.filter(
    #         **filters).order_by(ordering)
    #     serializer = self.get_serializer(event_queryset, many=True)
    #     return Response(serializer.data)
