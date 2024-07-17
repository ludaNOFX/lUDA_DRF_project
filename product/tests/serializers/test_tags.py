from rest_framework.test import APITestCase, APIRequestFactory
from product.models.tagproduct import TagProduct
from product.serializers.category import CategorySerializer
from product.serializers.tagproduct import TagsSerializer


class CategorySerializerTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.tag = TagProduct.objects.create(
            tag='Test Tag',
            slug='test-tag'
        )
        self.request = self.factory.get('/api/v1/category/')

    def test_serializer_fields(self):
        """Тестирование полей сериализатора"""
        serializer_context = {'request': self.request}
        serializer = TagsSerializer(instance=self.tag, context=serializer_context)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'url', 'tag', 'slug', 'products_url'})

    def test_serializer_read_only_fields(self):
        """Тестирование read_only_fields"""
        serializer_context = {'request': self.request}
        serializer = TagsSerializer(instance=self.tag, context=serializer_context)
        self.assertTrue('slug' in serializer.fields)
        self.assertTrue(serializer.fields['slug'].read_only)

    def test_serializer_extra_kwargs(self):
        """Тестирование extra_kwargs"""
        serializer_context = {'request': self.request}
        serializer = TagsSerializer(instance=self.tag, context=serializer_context)
        url_field = serializer.fields['url']
        self.assertEqual(url_field.lookup_field, 'slug')

    def test_get_products_url(self):
        """Тестирование метода get_products_url"""
        serializer_context = {'request': self.request}
        serializer = TagsSerializer(instance=self.tag, context=serializer_context)
        expected_url = self.request.build_absolute_uri(f'/api/v1/products/tags/{self.tag.slug}/products')
        self.assertEqual(serializer.data['products_url'], expected_url)

    def test_get_products_url_no_request(self):
        """Тестирование метода get_products_url при отсутствии request в контексте"""
        serializer = TagsSerializer(instance=self.tag)
        serializer.fields.pop('url')
        self.assertIsNone(serializer.data['products_url'])

    def test_serializer_invalid_data(self):
        """Тестирование сериализатора с некорректными данными"""
        data = {'tag': 'New Tag'}
        serializer = TagsSerializer(data=data, context={'request': self.request})
        self.assertTrue(serializer.is_valid())
