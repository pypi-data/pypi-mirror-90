from django.conf.urls import url
from bluedot_rest_framework import import_string


ChatConsumer = import_string('EVENT.chat.consumers')


websocket_urlpatterns = [
    url(r'ws/event/chat/(?P<event_id>\w+)', ChatConsumer),
]
