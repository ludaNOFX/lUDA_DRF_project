from django.test import TestCase
from django.urls import reverse

from product.models.category import Category


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Electronics')

    def test_category_creation(self):
        """Тестирование создания категории и её строкового представления"""
        self.assertEqual(self.category.name, 'Electronics')
        self.assertEqual(str(self.category), 'Electronics')

    def test_category_slug(self):
        """Тестирование автоматического создания slug при сохранении категории"""
        self.assertEqual(self.category.slug, 'electronics')

    def test_get_absolute_url(self):
        """Тестирование метода get_absolute_url"""
        url = self.category.get_absolute_url()
        expected_url = reverse('category-detail', kwargs={'slug': self.category.slug})
        self.assertEqual(url, expected_url)
