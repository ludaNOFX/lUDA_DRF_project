from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.test import APITestCase, APIRequestFactory

from product.models.category import Category
from product.models.detail import ProductDetail
from product.models.product import Product
from product.serializers.product_detail import ProductDetailSerializer

User = get_user_model()


class ProductDetailSerializerTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password123', slug='testuser-slug', email='testuser@mail.ru'
        )
        self.category = Category.objects.create(name='Category', slug='category')
        self.factory = APIRequestFactory()
        self.product = Product.objects.create(
            name='Test Product2',
            slug='test_product_slug2',
            description='Test description2',
            is_published=True,
            price=9.99,
            quantity=10,
            cat=self.category,
            user=self.user
        )
        self.product_detail = ProductDetail.objects.create(
            technical_details='test tech',
            slug='test_slug',
            color='red',
            material='cotton',
            product=self.product,
            weight=1,
            dimensions='1 kg'
        )
        self.request = self.factory.get('/api/v1/product-details/')
        self.request = Request(self.request)

    def test_serializer_fields(self):
        """Тестирование полей сериализатора"""
        serializer_context = {'request': self.request}
        serializer = ProductDetailSerializer(instance=self.product_detail, context=serializer_context)
        data = serializer.data
        self.assertEqual(set(data.keys()), {
            'url', 'technical_details', 'slug', 'product', 'color', 'weight', 'dimensions', 'material'})

    def test_serializer_read_only_fields(self):
        """Тестирование read_only_fields"""
        serializer_context = {'request': self.request}
        serializer = ProductDetailSerializer(instance=self.product_detail, context=serializer_context)
        self.assertTrue('slug' in serializer.fields)
        self.assertTrue(serializer.fields['slug'].read_only)

    def test_serializer_extra_kwargs(self):
        """Тестирование extra_kwargs"""
        serializer_context = {'request': self.request}
        serializer = ProductDetailSerializer(instance=self.product_detail, context=serializer_context)
        url_field = serializer.fields['url']
        self.assertEqual(url_field.lookup_field, 'slug')

    def test_serializer_invalid_data(self):
        """Тестирование сериализатора с некорректными данными"""
        data = {'product_detail': 'New product_detail'}
        serializer = ProductDetailSerializer(data=data, context={'request': self.request})
        self.assertTrue(serializer.is_valid())
