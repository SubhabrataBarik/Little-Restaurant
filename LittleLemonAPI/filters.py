import django_filters
from .models import MenuItem, Order

class MenuItemFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.NumberFilter(field_name='category__id', lookup_expr='exact')

    class Meta:
        model = MenuItem
        fields = ['category', 'price_min', 'price_max']


class OrderFilter(django_filters.FilterSet):
    total_min = django_filters.NumberFilter(field_name='total', lookup_expr='gte')
    total_max = django_filters.NumberFilter(field_name='total', lookup_expr='lte')
    date_after = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_before = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    delivery_crew = django_filters.NumberFilter(field_name='delivery_crew__id', lookup_expr='exact')
    user = django_filters.NumberFilter(field_name='user__id', lookup_expr='exact')

    class Meta:
        model = Order
        fields = ['status', 'delivery_crew', 'user', 'date_after', 'date_before', 'total_min', 'total_max']
