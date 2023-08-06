from django_filters import rest_framework as filters
from .models import User


class UserFilter(filters.FilterSet):
    wechat_profile__nick_name = filters.CharFilter(
        field_name='wechat_profile__nick_name', lookup_expr='contains')

    class Meta:
        model = User
        fields = ['wechat_profile__nick_name']
