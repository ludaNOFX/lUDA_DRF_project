from typing import List
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission
from rest_framework.request import Request
from rest_framework.response import Response
from product.models.manufacturer import Manufacturer
from rest_framework.decorators import action
from product.models.product import Product
from product.serializers.manufacturer import ManufacturerSerializer
from product.serializers.product import ProductSerializer
from product.utils.permissions import IsAdminOrOwner, IsOwnerOrReadOnly


class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    lookup_field = 'slug'

    @action(detail=True, methods=['get'])
    def products(self, request: Request, slug=None) -> Response:
        manufacturer = self.get_object()
        if request.user.is_authenticated and (request.user.is_staff or request.user == manufacturer.user):
            products = Product.objects.filter(manufacturer=manufacturer)
        else:
            products = Product.objects.filter(manufacturer=manufacturer, is_published=Product.Status.PUBLISHED)
        # products = Product.objects.filter(manufacturer=manufacturer).filter(is_published=Product.Status.PUBLISHED)
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

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
