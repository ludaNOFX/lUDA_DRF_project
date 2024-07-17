from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from product.models.category import Category
from product.models.manufacturer import Manufacturer
from product.models.product import Product
from product.models.tagproduct import TagProduct

User = get_user_model()


class ProductModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.category = Category.objects.create(name='Test Category')
        self.manufacturer = Manufacturer.objects.create(name='Test Manufacturer')
        self.tag1 = TagProduct.objects.create(tag='Tag 1')
        self.tag2 = TagProduct.objects.create(tag='Tag 2')

    def test_create_product(self):
        product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='This is a test product',
            price=10.50,
            quantity=20,
            cat=self.category,
            manufacturer=self.manufacturer,
            user=self.user
        )

        # Проверяем, что продукт был создан корректно
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.slug, 'test-product')
        self.assertEqual(product.description, 'This is a test product')
        self.assertEqual(product.price, 10.50)
        self.assertEqual(product.quantity, 20)
        self.assertEqual(product.cat, self.category)
        self.assertEqual(product.manufacturer, self.manufacturer)
        self.assertEqual(product.user, self.user)

        # Проверяем, что статус по умолчанию установлен в PUBLISHED
        self.assertEqual(product.is_published, Product.Status.PUBLISHED)

    def test_product_tags(self):
        product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='This is a test product',
            price=10.50,
            quantity=20,
            cat=self.category,
            manufacturer=self.manufacturer,
            user=self.user
        )
        product.tags.add(self.tag1, self.tag2)

        # Проверяем, что теги были добавлены к продукту
        self.assertIn(self.tag1, product.tags.all())
        self.assertIn(self.tag2, product.tags.all())

    def test_get_absolute_url(self):
        product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='This is a test product',
            price=10.50,
            quantity=20,
            cat=self.category,
            manufacturer=self.manufacturer,
            user=self.user
        )
        """Тестирование метода get_absolute_url"""
        url = product.get_absolute_url()
        expected_url = reverse('product-detail', kwargs={'slug': product.slug})
        self.assertEqual(url, expected_url)

    def test_published_manager(self):
        # Создаём несколько продуктов, один из которых будет черновиком
        published_product = Product.objects.create(
            name='Published Product',
            slug='published-product',
            description='Published product description',
            price=15.75,
            quantity=10,
            cat=self.category,
            manufacturer=self.manufacturer,
            user=self.user,
            is_published=Product.Status.PUBLISHED
        )
        draft_product = Product.objects.create(
            name='Draft Product',
            slug='draft-product',
            description='Draft product description',
            price=5.25,
            quantity=5,
            cat=self.category,
            manufacturer=self.manufacturer,
            user=self.user,
            is_published=Product.Status.DRAFT
        )

        # Проверяем, что только опубликованный продукт возвращается через published manager
        published_products = Product.published.all()
        self.assertIn(published_product, published_products)
        self.assertNotIn(draft_product, published_products)
