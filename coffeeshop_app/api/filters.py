from django_filters import rest_framework as filters
from coffeeshop_app.models import Item, Category

class PriceCategoryFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')
    categories = filters.ModelMultipleChoiceFilter(
        field_name='categories__id',
        to_field_name='id',
        queryset=Category.objects.all(),
        conjoined=True
    )

    class Meta:
        model = Item
        fields = ['price_min', 'price_max', 'categories']
