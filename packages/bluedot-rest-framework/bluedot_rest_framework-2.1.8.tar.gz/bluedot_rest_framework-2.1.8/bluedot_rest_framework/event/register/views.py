from rest_framework.decorators import action
from rest_framework.response import Response

from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, user_perform_create
from bluedot_rest_framework.utils.jwt_token import jwt_get_wechatid_handler


EventRegister = import_string('event.register.models')
EventRegisterSerializer = import_string('event.register.serializers')


class EventRegisterView(CustomModelViewSet):
    model_class = EventRegister
    serializer_class = EventRegisterSerializer
    filterset_fields = {
        'event_id': {
            'field_type': 'int',
            'lookup_expr': ''
        },
        'event_type': {
            'field_type': 'int',
            'lookup_expr': ''
        },
    }

    def perform_create(self, serializer):
        return user_perform_create(self.request.auth, serializer)

    @action(detail=False, methods=['get'], url_path='state', url_name='state')
    def state(self, request, *args, **kwargs):
        event_id = request.query_params.get('event_id', None)
        wechat_id = jwt_get_wechatid_handler(request.auth)
        queryset = self.model_class.objects.filter(
            wechat_id=wechat_id, event_id=event_id).first()
        state = -1
        if queryset:
            state = queryset.state
        return Response({'state': state})
