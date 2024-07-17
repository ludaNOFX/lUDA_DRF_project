from django.urls import path, register_converter, include
from .utils import converters
from rest_framework import routers
from .views.category import CategoryViewSet
from .views.manufacturer import ManufacturerViewSet
from .views.product import ProductViewSet
from .views.product_detail import ProductDetailReadOnlyViewSet
from .views.tag import TagsProductViewSet

router = routers.DefaultRouter()

router.register(r'product', ProductViewSet)
router.register(r'product-details', ProductDetailReadOnlyViewSet, basename='productdetail')
router.register(r'category', CategoryViewSet)
router.register(r'manufacturers', ManufacturerViewSet)
router.register(r'tags', TagsProductViewSet)

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', include(router.urls))
]
