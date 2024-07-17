from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField, QuerySet
from django.urls import reverse

from django_luda_project import settings
from .category import Category
from .manufacturer import Manufacturer
from .tagproduct import TagProduct


class PublishedManager(models.Manager):     # класс менеджер который возвращает только опублик записи
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_published=Product.Status.PUBLISHED)


class Product(models.Model):
    class Status(models.IntegerChoices):    # класс
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликованно'
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')
    image = models.ImageField(upload_to="images/%Y/%m/%d/", default=None,
                              blank=True, null=True, verbose_name="Изображение")
    description = models.TextField(blank=True, verbose_name='Описание')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.PUBLISHED, verbose_name='Статус')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')        # цена товара
    quantity = models.PositiveIntegerField(default=0, verbose_name='Кол-во')      # кол-во товара только полож цел числа
    cat = models.ForeignKey(Category, on_delete=models.PROTECT,
                            related_name='products', verbose_name="Категории")    # связь с табл Категории
    tags = models.ManyToManyField(TagProduct, blank=True,
                                  related_name='products', verbose_name='Теги')      # сязь с табл Тэги продуктов
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.PROTECT, related_name='products',
                                     null=True, blank=True,
                                     verbose_name='Производитель')   # связь с Производителями один произв много продукт
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE,
                             related_name='products')

    objects = models.Manager()      # стандартный менеджер чтобы он тоже работал
    published = PublishedManager()      # атрибут менеджер созданный мной

    def __str__(self) -> CharField:
        return self.name

    class Meta:     # вложенный класс тут я сделал сортировку по убыванию и добавил индексирование по умолчанию
        verbose_name = "Продукты"
        verbose_name_plural = "Продукты"
        ordering = ['-time_create']     # сортировка по полю time_create по убыванию
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self) -> str:
        return reverse('product-detail', kwargs={'slug': self.slug})



