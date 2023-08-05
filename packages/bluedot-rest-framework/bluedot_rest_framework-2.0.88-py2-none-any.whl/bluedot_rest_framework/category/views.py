from rest_framework.decorators import action
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, TreeAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Category
from .serializers import CategorySerializer
from rest_framework.filters import OrderingFilter
from .filter import CategoryFilter
from rest_framework import filters
from django_filters.rest_framework.backends import DjangoFilterBackend


class CategoryView(CustomModelViewSet, TreeAPIView):
    model_class = Category
    serializer_class = CategorySerializer
    pagination_class = None
    filterset_class = CategoryFilter
    filter_backends = [
        DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = '__all__'
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['post'], url_path='sort', url_name='sort')
    def sort(self, request, *args, **kwargs):
        before_sort = request.data.get('before_sort')
        before_id = request.data.get('before_id')
        after_sort = request.data.get('after_sort')
        after_id = request.data.get('after_id')
        self.model_class.objects.get(pk=before_id).update(sort=after_sort)
        self.model_class.objects.get(pk=after_id).update(sort=before_sort)
        return Response(status=200)
