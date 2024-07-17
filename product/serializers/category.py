from typing import Optional
from rest_framework import serializers
from rest_framework.request import Request
from product.models.category import Category
from product.models.product import Product


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    products_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['slug', 'product']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

    def get_products_url(self, obj: Category) -> Optional[Request]:
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/v1/products/category/{obj.slug}/products')
        return None
