from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from product.models.manufacturer import Manufacturer


class ManufacturerModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.manufacturer = Manufacturer.objects.create(
            name='Test Manufacturer',
            address='123 Test St, Test City',
            website='http://testmanufacturer.com',
            product_count=10,
            user=self.user
        )

    def test_manufacturer_creation(self):
        """Тестирование создания производителя и его строкового представления"""
        self.assertEqual(self.manufacturer.name, 'Test Manufacturer')
        self.assertEqual(str(self.manufacturer), 'Test Manufacturer')

    def test_manufacturer_slug(self):
        """Тестирование автоматического создания slug при сохранении производителя"""
        self.assertEqual(self.manufacturer.slug, 'test-manufacturer')

    def test_get_absolute_url(self):
        """Тестирование метода get_absolute_url"""
        url = self.manufacturer.get_absolute_url()
        expected_url = reverse('manufacturer-detail', kwargs={'slug': self.manufacturer.slug})
        self.assertEqual(url, expected_url)

    def test_manufacturer_blank_fields(self):
        """Тестирование полей, которые могут быть пустыми"""
        manufacturer_blank = Manufacturer.objects.create(
            name='Blank Manufacturer',
        )
        self.assertEqual(manufacturer_blank.address, '')
        self.assertEqual(manufacturer_blank.website, '')
        self.assertEqual(manufacturer_blank.product_count, 0)
        self.assertIsNone(manufacturer_blank.user)

    def test_manufacturer_with_user(self):
        """Тестирование случая, когда пользователь назначен"""
        self.assertEqual(self.manufacturer.user, self.user)
        self.assertEqual(self.user.company, self.manufacturer)
