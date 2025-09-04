from django import forms
from django_filters import rest_framework as filters
from coffeeshop_app.models import Item, Category


class CommaSeparatedModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def clean(self, value):
        if isinstance(value, str):
            value = value.split(",")
        elif isinstance(value, list) and len(value) == 1 and "," in value[0]:
            value = value[0].split(",")
        return super().clean(value)


class CommaSeparatedModelMultipleChoiceFilter(filters.ModelMultipleChoiceFilter):
    field_class = CommaSeparatedModelMultipleChoiceField


class PriceCategoryFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = filters.NumberFilter(field_name="price", lookup_expr="lte")
    categories = CommaSeparatedModelMultipleChoiceFilter(
        field_name="categories__id",
        to_field_name="id",
        queryset=Category.objects.all(),
        conjoined=True,
    )

    class Meta:
        model = Item
        fields = ["price_min", "price_max", "categories"]
