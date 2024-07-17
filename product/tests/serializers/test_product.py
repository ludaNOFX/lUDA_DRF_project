from decimal import Decimal

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.request import Request
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from django.contrib.auth import get_user_model

from product.models.category import Category
from product.models.detail import ProductDetail
from product.models.manufacturer import Manufacturer
from product.models.product import Product
from product.models.tagproduct import TagProduct
from product.serializers.product import ProductSerializer

User = get_user_model()


class ProductSerializerTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser', password='password123', slug='testuser-slug', email='testuser@mail.ru'
        )
        self.tag1 = TagProduct.objects.create(tag='Tag1', slug='tag1')
        self.tag2 = TagProduct.objects.create(tag='Tag2', slug='tag2')
        self.category = Category.objects.create(name='Category', slug='category')
        self.manufacturer = Manufacturer.objects.create(name='Manufacturer', slug='manufacturer')

        # Используем slug для URL в self.product_data
        self.product_data = {
            'name': 'Test Product',
            'description': 'Test description',
            'is_published': True,
            'price': 9.99,
            'quantity': 10,
            'cat': self.category.get_absolute_url(),  # Используем slug модели Category
            'manufacturer': self.manufacturer.get_absolute_url(),  # Используем slug модели Manufacturer
            'tags': [
                self.tag1.get_absolute_url(),
                self.tag2.get_absolute_url(),  # Используем slug модели TagProduct
                # self.tag2.slug  # Используем slug модели TagProduct
            ],
            'detail': {
                'weight': 1,
                'dimensions': '1 kg'
            }
        }

        self.product = Product.objects.create(
            name='Test Product2',
            slug='test_product_slug2',
            description='Test description2',
            is_published=True,
            price=9.99,
            quantity=10,
            cat=self.category,
            manufacturer=self.manufacturer,
            user=self.user
        )
        self.product.tags.set([self.tag1, self.tag2])
        self.product_detail = ProductDetail.objects.create(
            slug='test-detail-slug',
            product=self.product,
            weight=1,
            dimensions='1 kg'
        )

    def test_serializer_fields(self):
        """Тестирование полей сериализатора"""
        request = self.factory.get('/api/v1/products/')
        request = Request(request)
        force_authenticate(request, user=self.user)
        request.user = self.user
        serializer_context = {'request': request}
        serializer = ProductSerializer(data=self.product_data, context=serializer_context)
        serializer.is_valid()
        serializer.save()
        data = serializer.data
        data['user'] = request.user
        self.assertIn('name', data)
        self.assertEqual(data['name'], 'Test Product')

        self.assertEqual(set(data.keys()), {'url', 'id', 'user', 'user_url', 'name', 'slug', 'image', 'description',
                                            'time_create', 'time_update', 'is_published', 'price', 'quantity', 'cat',
                                            'manufacturer', 'tags_url', 'tags', 'detail'})
        self.assertEqual(data['user'], self.user)
        self.assertEqual((data['cat']), reverse(
            'category-detail', kwargs={'slug': self.category.slug}, request=request))
        self.assertEqual(data['manufacturer'], reverse(
            'manufacturer-detail', kwargs={'slug': self.manufacturer.slug}, request=request))
        self.assertEqual(data['tags_url'], reverse(
            'product-tags', kwargs={'slug': data['slug']}, request=request))
        self.assertIn('detail', data)

    def test_serializer_read_only_fields(self):
        """Тестирование read_only_fields"""
        request = self.factory.get('/api/v1/products/')
        force_authenticate(request, user=self.user)
        request.user = self.user
        serializer_context = {'request': request}
        serializer = ProductSerializer(instance=self.product, context=serializer_context)
        data = serializer.data
        self.assertTrue('slug' in serializer.fields)
        self.assertTrue(serializer.fields['slug'].read_only)
        self.assertTrue('user' in serializer.fields)

    def test_get_user_url(self):
        """Тестирование метода get_user_url"""
        request = self.factory.get('/api/v1/products/')
        force_authenticate(request, user=self.user)
        # # request.user = self.user
        serializer_context = {'request': request}
        serializer = ProductSerializer(instance=self.product, context=serializer_context)
        expected_url = request.build_absolute_uri(f'/api/v1/accounts/{self.user.slug}')
        self.assertEqual(serializer.data['user_url'], expected_url)

    def test_get_tags_url(self):
        """Тестирование метода get_tags_url"""
        request = self.factory.get('/api/v1/products/')
        force_authenticate(request, user=self.user)
        request.user = self.user
        serializer_context = {'request': request}
        serializer = ProductSerializer(instance=self.product, context=serializer_context)
        expected_url = request.build_absolute_uri(f'/api/v1/products/product/{self.product.slug}/tags/')
        self.assertEqual(serializer.data['tags_url'], expected_url)

    def test_create_product(self):
        """Тестирование создания продукта"""
        request = self.factory.post('/api/v1/products/', self.product_data, format='json')
        force_authenticate(request, user=self.user)
        request.user = self.user
        serializer_context = {'request': request}
        serializer = ProductSerializer(data=self.product_data, context=serializer_context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        product = serializer.save()
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.user, self.user)
        self.assertEqual(product.cat, self.category)
        self.assertEqual(product.manufacturer, self.manufacturer)
        self.assertEqual(list(product.tags.all()), [self.tag1, self.tag2])
        self.assertTrue(hasattr(product, 'detail'))
        self.assertEqual(product.detail.weight, 1)
        self.assertEqual(product.detail.dimensions, '1 kg')

    def test_update_product(self):
        """Тестирование обновления продукта"""
        updated_data = {
            'name': 'Updated Product',
            'description': 'Updated description',
            'price': 19.99,
            'quantity': 5,
            'detail': {
                'weight': 15
            }
        }
        request = self.factory.put(f'/api/v1/products/{self.product.slug}/', updated_data, format='json')
        force_authenticate(request, user=self.user)
        request.user = self.user
        serializer_context = {'request': request}
        serializer = ProductSerializer(instance=self.product, data=updated_data, context=serializer_context, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_product = serializer.save()
        self.assertEqual(updated_product.name, 'Updated Product')
        self.assertEqual(updated_product.description, 'Updated description')
        self.assertEqual(updated_product.price,  Decimal('19.99'))
        self.assertEqual(updated_product.quantity, 5)
        self.assertEqual(updated_product.detail.weight, 15)
