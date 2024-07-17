from django.db import models
from django.db.models import CharField
from django.urls import reverse
from pytils.translit import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> CharField:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse('category-detail', kwargs={'slug': self.slug})

    def save(self, *args: tuple, **kwargs: dict) -> None:
        self.slug: str = slugify(self.name)
        super().save(*args, **kwargs)
