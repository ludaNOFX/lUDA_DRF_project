from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django_luda_project import settings
from pytils.translit import slugify


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    product_count = models.IntegerField(blank=True, default=0)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='company', blank=True, null=True, verbose_name='Владелец Компании')

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"

    def __str__(self) -> CharField:
        return self.name

    def get_absolute_url(self):
        return reverse('manufacturer-detail', kwargs={'slug': self.slug})

    def save(self, *args: tuple, **kwargs: dict) -> None:
        self.slug: str = slugify(self.name)
        super().save(*args, **kwargs)
