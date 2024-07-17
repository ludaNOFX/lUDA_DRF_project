from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from product.models.category import Category
from product.models.detail import ProductDetail
from product.models.product import Product


class ProductDetailModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            user=self.user,
            cat=self.category,
            price=100,
            quantity=10,
            is_published=Product.Status.PUBLISHED,
        )
        self.product_detail = ProductDetail.objects.create(
            product=self.product,
            technical_details='Technical details of test product',
            slug='test-product-detail',
            dimensions='100x200x300',
            weight=1.5,
            color='Red',
            material='Plastic'
        )

    def test_product_detail_creation(self):
        """Тестирование создания деталей продукта и её строкового представления"""
        self.assertEqual(self.product_detail.product, self.product)
        self.assertEqual(str(self.product_detail), 'Детали продукта: Test Product')

    def test_product_detail_slug(self):
        """Тестирование автоматического создания slug при сохранении деталей продукта"""
        self.assertEqual(self.product_detail.slug, 'test-product-detail')

    def test_get_absolute_url(self):
        """Тестирование метода get_absolute_url"""
        url = self.product_detail.get_absolute_url()
        expected_url = reverse('productdetail-detail', kwargs={'slug': self.product_detail.slug})
        self.assertEqual(url, expected_url)

    def test_product_detail_blank_fields(self):
        """Тестирование полей, которые могут быть пустыми"""
        new_product = Product.objects.create(
            name='Test Product 2',
            slug='test-product-2',
            user=self.user,
            cat=self.category,
            price=200,
            quantity=20,
            is_published=Product.Status.PUBLISHED,
        )
        product_detail_blank = ProductDetail.objects.create(
            product=new_product,
            slug='test-product-detail-blank'
        )
        self.assertEqual(product_detail_blank.technical_details, '')
        self.assertEqual(product_detail_blank.dimensions, '')
        self.assertEqual(product_detail_blank.weight, None)
        self.assertEqual(product_detail_blank.color, '')
        self.assertEqual(product_detail_blank.material, '')

    def test_product_detail_no_product(self):
        """Тестирование случая, когда продукт не назначен"""
        product_detail_no_product = ProductDetail.objects.create(
            technical_details='No product',
            slug='no-product-detail'
        )
        self.assertEqual(str(product_detail_no_product), 'Детали продукта: не назначен')
