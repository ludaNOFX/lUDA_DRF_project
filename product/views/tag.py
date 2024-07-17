from typing import List
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, BasePermission
from rest_framework.request import Request
from rest_framework.response import Response
from product.models.product import Product
from product.models.tagproduct import TagProduct
from product.serializers.product import ProductSerializer
from product.serializers.tagproduct import TagsSerializer


class TagsProductViewSet(viewsets.ModelViewSet):
    queryset = TagProduct.objects.all()
    serializer_class = TagsSerializer
    lookup_field = 'slug'

    @action(detail=True, methods=['get'])
    def products(self, request: Request, slug=None) -> Response:
        tag = self.get_object()
        products = Product.objects.filter(tags=tag).filter(is_published=Product.Status.PUBLISHED)
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

    def get_permissions(self) -> List[BasePermission]:
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
