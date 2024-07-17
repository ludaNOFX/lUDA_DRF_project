from rest_framework import serializers
from product.models.detail import ProductDetail


class ProductDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductDetail
        fields = '__all__'
        read_only_fields = ['slug', 'product']

        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
            'product': {'lookup_field': 'slug'},
        }


