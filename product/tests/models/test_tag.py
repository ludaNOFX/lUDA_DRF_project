from django.test import TestCase
from django.urls import reverse
from product.models.tagproduct import TagProduct


class TagProductModelTest(TestCase):

    def setUp(self):
        self.tag = TagProduct.objects.create(
            tag='Test Tag'
        )

    def test_tag_creation(self):
        """Тестирование создания тега и его строкового представления"""
        self.assertEqual(self.tag.tag, 'test tag')
        self.assertEqual(str(self.tag), 'test tag')

    def test_tag_slug(self):
        """Тестирование автоматического создания slug при сохранении тега"""
        self.assertEqual(self.tag.slug, 'test-tag')

    def test_get_absolute_url(self):
        """Тестирование метода get_absolute_url"""
        url = self.tag.get_absolute_url()
        expected_url = reverse('tagproduct-detail', kwargs={'slug': self.tag.slug})
        self.assertEqual(url, expected_url)

    def test_tag_field_db_index(self):
        """Тестирование наличия индекса на поле tag"""
        field_indexed = TagProduct._meta.get_field('tag').db_index
        self.assertTrue(field_indexed)

    def test_slug_field_db_index(self):
        """Тестирование наличия индекса на поле slug"""
        field_indexed = TagProduct._meta.get_field('slug').db_index
        self.assertTrue(field_indexed)

    def test_slug_field_unique(self):
        """Тестирование уникальности поля slug"""
        field_unique = TagProduct._meta.get_field('slug').unique
        self.assertTrue(field_unique)
