from typing import Optional

from rest_framework import serializers
from rest_framework.request import Request

from product.models.product import Product
from product.models.tagproduct import TagProduct


class TagsSerializer(serializers.HyperlinkedModelSerializer):
    products_url = serializers.SerializerMethodField()

    class Meta:
        model = TagProduct
        fields = '__all__'
        read_only_fields = ['slug']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

    def get_products_url(self, obj: TagProduct) -> Optional[Request]:
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/v1/products/tags/{obj.slug}/products')
        return None
