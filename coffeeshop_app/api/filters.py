from django_filters import rest_framework as filters
from coffeeshop_app.models import Item

class ItemFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Item
        fields = ['price_min', 'price_max']
