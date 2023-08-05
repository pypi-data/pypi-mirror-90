
from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, user_perform_create, AllView

EventChat = import_string('EVENT.chat.models')
EventChatSerializer = import_string('EVENT.chat.serializers')


class EventChatView(CustomModelViewSet, AllView):
    model_class = EventChat
    serializer_class = EventChatSerializer
    filterset_fields = {
        'event_id': ['exact'],
        'state': ['exact']
    }

    def perform_create(self, serializer):
        return user_perform_create(self.request.auth, serializer)
