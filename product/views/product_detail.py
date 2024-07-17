from rest_framework import viewsets
from product.models.detail import ProductDetail
from product.serializers.product_detail import ProductDetailSerializer


class ProductDetailReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductDetail.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'
