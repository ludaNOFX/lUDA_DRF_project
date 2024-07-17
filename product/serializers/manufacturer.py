from typing import Optional
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.request import Request
from product.models.manufacturer import Manufacturer
from product.models.product import Product

User = get_user_model()


class ManufacturerSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    products_url = serializers.SerializerMethodField()
    user_url = serializers.SerializerMethodField()

    class Meta:
        model = Manufacturer
        fields = ['url', 'id', 'user', 'user_url', 'name', 'slug',
                  'address', 'website', 'product_count', 'products_url']
        read_only_fields = ['slug', 'product_count']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

    def get_user_url(self, obj: Manufacturer) -> Optional[Request]:
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/v1/accounts/{obj.user.slug}')
        return None

    def get_products_url(self, obj: Manufacturer) -> Optional[Request]:
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/v1/products/manufacturers/{obj.slug}/products')
        return None
