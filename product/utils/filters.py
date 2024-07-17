import django_filters
from product.models.product import Product


class ProductTagFilter(django_filters.FilterSet):
    tags__tag = django_filters.CharFilter(field_name='tags__tag', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['tags__tag']

