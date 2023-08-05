from rest_framework.decorators import action
from rest_framework.response import Response
from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, user_perform_create, AllView
from bluedot_rest_framework.utils.jwt_token import jwt_get_userid_handler
from rest_framework import filters
from django_filters.rest_framework.backends import DjangoFilterBackend
from .filter import EventCommentFilter

EventComment = import_string('EVENT.comment.models')
EventCommentSerializer = import_string('EVENT.comment.serializers')
EventCommentLike = import_string('EVENT.comment.like_models')
EventCommentLikeSerializer = import_string('EVENT.comment.like_serializers')


class EventCommentView(CustomModelViewSet):
    model_class = EventComment
    serializer_class = EventCommentSerializer
    filterset_class = EventCommentFilter
    filter_backends = [
        DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = '__all__'

    def perform_create(self, serializer):
        return user_perform_create(self.request.auth, serializer)

    @action(detail=False, methods=['get'], url_path='show', url_name='show')
    def show(self, request, *args, **kwargs):
        user_id = jwt_get_userid_handler(request.auth)
        queryset = self.filter_queryset(self.get_queryset())
        data = self.get_serializer(queryset, many=True).data
        for item in data:
            item['is_like'] = 0
            if EventCommentLike.objects.filter(user_id=user_id, comment_id=item['id']):
                item['is_like'] = 1
        return Response(data)


class EventCommentLikeView(CustomModelViewSet):
    model_class = EventCommentLike
    serializer_class = EventCommentLikeSerializer
