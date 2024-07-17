from rest_framework.test import APITestCase, APIRequestFactory
from product.models.category import Category
from product.serializers.category import CategorySerializer


class CategorySerializerTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.request = self.factory.get('/api/v1/category/')

    def test_serializer_fields(self):
        """Тестирование полей сериализатора"""
        serializer_context = {'request': self.request}
        serializer = CategorySerializer(instance=self.category, context=serializer_context)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'url', 'name', 'slug', 'products_url'})

    def test_serializer_read_only_fields(self):
        """Тестирование read_only_fields"""
        serializer_context = {'request': self.request}
        serializer = CategorySerializer(instance=self.category, context=serializer_context)
        self.assertTrue('slug' in serializer.fields)
        self.assertTrue(serializer.fields['slug'].read_only)

    def test_serializer_extra_kwargs(self):
        """Тестирование extra_kwargs"""
        serializer_context = {'request': self.request}
        serializer = CategorySerializer(instance=self.category, context=serializer_context)
        url_field = serializer.fields['url']
        self.assertEqual(url_field.lookup_field, 'slug')

    def test_get_products_url(self):
        """Тестирование метода get_products_url"""
        serializer_context = {'request': self.request}
        serializer = CategorySerializer(instance=self.category, context=serializer_context)
        expected_url = self.request.build_absolute_uri(f'/api/v1/products/category/{self.category.slug}/products')
        self.assertEqual(serializer.data['products_url'], expected_url)

    def test_get_products_url_no_request(self):
        """Тестирование метода get_products_url при отсутствии request в контексте"""
        serializer = CategorySerializer(instance=self.category)
        serializer.fields.pop('url')
        self.assertIsNone(serializer.data['products_url'])

    def test_serializer_invalid_data(self):
        """Тестирование сериализатора с некорректными данными"""
        data = {'name': 'New Category'}
        serializer = CategorySerializer(data=data, context={'request': self.request})
        self.assertTrue(serializer.is_valid())

