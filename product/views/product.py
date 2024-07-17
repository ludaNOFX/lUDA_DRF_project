from typing import List, Union
from django_filters import rest_framework as filters
from rest_framework import viewsets
from django.db.models import Q, QuerySet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission
from rest_framework.request import Request
from rest_framework.response import Response

from product.models.product import Product
from product.serializers.tagproduct import TagsSerializer
from product.utils.filters import ProductTagFilter
from product.utils.pagination import ProductAPIListPagination
from product.utils.permissions import IsOwnerOrReadOnly, IsAdminOrOwner
from product.serializers.product import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ProductTagFilter
    pagination_class = ProductAPIListPagination
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

    def get_queryset(self) -> Union[QuerySet[Product], QuerySet]:
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            # Если пользователь администратор, показываем все записи
            return Product.objects.all()
        elif user.is_authenticated:
            # Если пользователь авторизован, показываем только опубликованные записи и свои неопубликованные
            return Product.objects.filter(Q(is_published=Product.Status.PUBLISHED) |
                                          Q(is_published=Product.Status.DRAFT, user=user))
        else:
            # Если пользователь не авторизован, показываем только опубликованные записи
            return Product.objects.filter(is_published=Product.Status.PUBLISHED)

    @action(detail=True, methods=['get'])
    def tags(self, request: Request, slug=None) -> Response:
        product = self.get_object()
        tags = product.tags.filter(products=product)
        serializer = TagsSerializer(tags, many=True, context={'request': request})
        return Response(serializer.data)
