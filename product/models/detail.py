from typing import Union

from django.db import models
from django.db.models import CharField
from django.urls import reverse


class ProductDetail(models.Model):
    technical_details = models.TextField(blank=True, verbose_name='Технические характеристики')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug-detail')
    dimensions = models.CharField(max_length=100, blank=True, verbose_name='Размеры')
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name='Вес')
    color = models.CharField(max_length=30, blank=True, verbose_name='Цвет')
    material = models.CharField(max_length=30, blank=True, verbose_name='Материал')
    product = models.OneToOneField('Product', on_delete=models.CASCADE,
                                   related_name='detail', blank=True, null=True, verbose_name='Продукт')

    def __str__(self) -> Union[CharField, str]:
        if self.product:
            return f"Детали продукта: {self.product.name}"
        return "Детали продукта: не назначен"

    class Meta:
        verbose_name = "Детали о продукте"
        verbose_name_plural = "Детали о продукте"

    def get_absolute_url(self):
        return reverse('productdetail-detail', kwargs={'slug': self.slug})


