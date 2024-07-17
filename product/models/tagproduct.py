from django.db import models
from django.db.models import CharField
from django.urls import reverse
from pytils.translit import slugify


class TagProduct(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self) -> str:
        return self.tag

    def get_absolute_url(self) -> str:
        return reverse('tagproduct-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs) -> None:
        self.tag: str = str(self.tag).lower()  # Приведение к нижнему регистру перед сохранением
        self.slug: str = slugify(self.tag)
        super().save(*args, **kwargs)
