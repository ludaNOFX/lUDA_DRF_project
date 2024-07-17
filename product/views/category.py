from typing import List
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, BasePermission
from rest_framework.request import Request
from rest_framework.response import Response
from product.models.category import Category
from product.models.product import Product
from product.serializers.category import CategorySerializer
from product.serializers.product import ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    @action(detail=True, methods=['get'])
    def products(self, request: Request, slug=None) -> Response:
        category = self.get_object()
        products = Product.objects.filter(cat=category).filter(is_published=Product.Status.PUBLISHED)
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

    def get_permissions(self) -> List[BasePermission]:
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
