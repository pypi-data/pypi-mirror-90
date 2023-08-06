from django_filters import rest_framework as filters
from .models import Category


class CategoryFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='contains')
    category_type = filters.NumberFilter(
        field_name='category_type', lookup_expr='exact')

    class Meta:
        model = Category
        fields = ['title', 'category_type']
