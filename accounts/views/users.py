from typing import List
from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from accounts.serializers.users import UserSerializer
from product.models.product import Product
from product.serializers.product import ProductSerializer
from accounts.utils.permissions import IsAdminOrOwner, IsOwnerOrReadOnly


User = get_user_model()


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'slug'

    def get_permissions(self) -> List[BasePermission]:
        """
        Инстанцирует и возвращает список пермишенов, которые требуются для данного представления.
        """
        if self.action in ['retrieve', 'list']:
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action == 'destroy':
            permission_classes = [IsAdminOrOwner]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'])
    def products(self, request: Request, slug=None) -> Response:
        user = self.get_object()
        if request.user.is_authenticated and (request.user.is_staff or request.user == user):
            products = Product.objects.filter(user=user)
        else:
            products = Product.objects.filter(user=user, is_published=Product.Status.PUBLISHED)

        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def followers(self, request: Request, slug=None) -> Response:
        user = self.get_object()
        followers = user.followed.all()
        serializer = UserSerializer(followers, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def following(self, request: Request, slug=None) -> Response:
        user = self.get_object()
        following = user.following.all()
        serializer = UserSerializer(following, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def following_users_products(self, request: Request, slug=None) -> Response:
        user = self.get_object()
        following_users = user.following.all()

        if request.user.is_authenticated:
            if request.user.is_staff:
                products = Product.objects.filter(user__in=following_users)
            else:
                products = Product.objects.filter(user__in=following_users, is_published=Product.Status.PUBLISHED)

            serializer = ProductSerializer(products, many=True, context={'request': request})

            return Response(serializer.data)




