from typing import Optional, List
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from product.models.product import Product

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    products_url = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    following_users_products = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'url', 'slug', 'username', 'company',
                  'photo', 'email', 'date_birth', 'first_name',
                  'last_name', 'products_url', 'following_users_products', 'followers', 'following')
        read_only_fields = ['slug',]
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
            'company': {'lookup_field': 'slug'}
        }

    def get_products_url(self, obj: User) -> Optional[str]:
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/v1/accounts/{obj.slug}/products')
        return None

    def get_followers(self, obj: User) -> Optional[str]:
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/v1/accounts/{obj.slug}/followers')
        return None

    def get_following(self, obj: User) -> Optional[str]:
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/v1/accounts/{obj.slug}/following')
        return None

    def get_following_users_products(self, obj: User) -> Optional[str]:
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/v1/accounts/{obj.slug}/following_users_products')
        return None




