from typing import Any, Optional, Dict

from django.contrib.auth import get_user_model
from pytils.translit import slugify
from rest_framework import serializers
from rest_framework.request import Request

from product.models.category import Category
from product.models.detail import ProductDetail
from product.models.manufacturer import Manufacturer
from product.models.product import Product
from product.models.tagproduct import TagProduct
from product.serializers.product_detail import ProductDetailSerializer

User = get_user_model()


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_url = serializers.SerializerMethodField()
    tags_url = serializers.SerializerMethodField()
    detail = ProductDetailSerializer(required=False)

    class Meta:
        model = Product
        fields = ['url', 'id', 'user', 'user_url', 'name', 'slug', 'image', 'description', 'time_create',
                  'time_update', 'is_published', 'price', 'quantity', 'cat',
                  'manufacturer', 'tags_url', 'tags', 'detail']
        read_only_fields = ['slug', 'user']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
            'tags': {'lookup_field': 'slug'},
            'cat': {'lookup_field': 'slug'},
            'manufacturer': {'lookup_field': 'slug'},
        }

    def get_user_url(self, obj: Product) -> Optional[Request]:
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/v1/accounts/{obj.user.slug}')
        return None

    def get_tags_url(self, obj: Product) -> Optional[Request]:
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/v1/products/product/{obj.slug}/tags/')
        return None

    def create(self, validated_data: Optional[Dict[str, Any]]) -> Product:
        self.context.get('request')
        detail_data: Optional[Dict[str, Any]] = validated_data.pop('detail', None)
        slug: str = slugify(validated_data['name'])
        validated_data['slug'] = slug
        product: Product = super().create(validated_data)
        if detail_data and any(detail_data.values()):
            detail_data['product'] = product
            detail_data['slug'] = slug + '-detail'
            ProductDetail.objects.create(**detail_data)
        return product

    def update(self, instance: Product, validated_data: Optional[Dict[str, Any]]) -> Product:
        # Обновление основных полей продукта
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.is_published = validated_data.get('is_published', instance.is_published)
        instance.price = validated_data.get('price', instance.price)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.cat = validated_data.get('cat', instance.cat)
        instance.manufacturer = validated_data.get('manufacturer', instance.manufacturer)
        if 'tags' in validated_data:
            instance.tags.set(validated_data['tags'])
        instance.save()

        # Обновление вложенного сериализатора ProductDetailSerializer
        detail_data: Optional[Dict[str, Any]] = validated_data.get('detail')
        if detail_data and any(detail_data.values()):
            if hasattr(instance, 'detail'):
                detail_instance: ProductDetail = instance.detail
                for attr, value in detail_data.items():
                    setattr(detail_instance, attr, value)
                detail_instance.save()
            else:
                detail_data['product'] = instance
                detail_data['slug'] = f"{instance.slug}-detail"
                ProductDetail.objects.create(**detail_data)

        return instance

