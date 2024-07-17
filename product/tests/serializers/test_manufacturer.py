
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from django.contrib.auth import get_user_model
from product.models.manufacturer import Manufacturer
from product.serializers.manufacturer import ManufacturerSerializer

User = get_user_model()


class ManufacturerSerializerTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser', password='password123', slug='testuser-slug'
        )
        self.manufacturer = Manufacturer.objects.create(
            name='Test Manufacturer',
            slug='test-manufacturer',
            address='123 Test Street',
            website='https://www.testmanufacturer.com',
            product_count=10,
            user=self.user
        )

    def test_serializer_fields(self):
        """Тестирование полей сериализатора"""
        request = self.factory.get('/api/v1/manufacturers/')
        force_authenticate(request, user=self.user)
        serializer_context = {'request': request}
        serializer = ManufacturerSerializer(instance=self.manufacturer, context=serializer_context)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'url', 'id', 'user_url', 'name', 'slug',
                                            'address', 'website', 'product_count', 'products_url'})

    def test_serializer_read_only_fields(self):
        """Тестирование read_only_fields"""
        request = self.factory.get('/api/v1/manufacturers/')
        force_authenticate(request, user=self.user)
        serializer_context = {'request': request}
        serializer = ManufacturerSerializer(instance=self.manufacturer, context=serializer_context)
        data = serializer.data
        self.assertTrue('slug' in serializer.fields)
        self.assertTrue('product_count' in serializer.fields)
        self.assertTrue(serializer.fields['slug'].read_only)
        self.assertTrue(serializer.fields['product_count'].read_only)

    def test_serializer_extra_kwargs(self):
        """Тестирование extra_kwargs"""
        request = self.factory.get('/api/v1/manufacturers/')
        force_authenticate(request, user=self.user)
        serializer_context = {'request': request}
        serializer = ManufacturerSerializer(instance=self.manufacturer, context=serializer_context)
        url_field = serializer.fields['url']
        self.assertEqual(url_field.lookup_field, 'slug')

    def test_get_user_url(self):
        """Тестирование метода get_user_url"""
        request = self.factory.get('/api/v1/manufacturers/')
        force_authenticate(request, user=self.user)
        serializer_context = {'request': request}
        serializer = ManufacturerSerializer(instance=self.manufacturer, context=serializer_context)
        expected_url = request.build_absolute_uri(f'/api/v1/accounts/{self.user.slug}')
        self.assertEqual(serializer.data['user_url'], expected_url)

    def test_get_user_url_no_request(self):
        """Тестирование метода get_user_url при отсутствии request в контексте"""
        serializer = ManufacturerSerializer(instance=self.manufacturer)
        serializer.fields.pop('url')
        self.assertIsNone(serializer.data['user_url'])

    def test_get_products_url(self):
        """Тестирование метода get_products_url"""
        request = self.factory.get('/api/v1/manufacturers/')
        force_authenticate(request, user=self.user)
        serializer_context = {'request': request}
        serializer = ManufacturerSerializer(instance=self.manufacturer, context=serializer_context)
        expected_url = request.build_absolute_uri(f'/api/v1/products/manufacturers/{self.manufacturer.slug}/products')
        self.assertEqual(serializer.data['products_url'], expected_url)

    def test_get_products_url_no_request(self):
        """Тестирование метода get_products_url при отсутствии request в контексте"""
        serializer = ManufacturerSerializer(instance=self.manufacturer)
        serializer.fields.pop('url')
        self.assertIsNone(serializer.data['products_url'])
