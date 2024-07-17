from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from pytils.translit import slugify


class User(AbstractUser):
    photo = models.ImageField(upload_to="images/%Y/%m/%d/", default=None,
                              blank=True, null=True, verbose_name="Фотография")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')
    email = models.EmailField(unique=True)
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name="Дата Рождения")
    followed = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                      related_name='following', verbose_name='Подписанные')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def follow(self, user: 'User') -> None:
        """
        Подписывает текущего пользователя на указанного пользователя.
        """
        if not self.is_following(user):
            self.followed.add(user)
            self.save()
            user.save()

    def unfollow(self, user: 'User') -> None:
        """
        Отписывает текущего пользователя от указанного пользователя.
        """
        if self.is_following(user):
            self.followed.remove(user)
            self.save()
            user.save()

    def is_following(self, user: 'User') -> bool:
        """
        Проверяет, подписан ли текущий пользователь на указанного пользователя.
        """
        return self.followed.filter(pk=user.pk).exists()

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.username)  # Генерируем slug при сохранении, если он не задан
        super().save(*args, **kwargs)



