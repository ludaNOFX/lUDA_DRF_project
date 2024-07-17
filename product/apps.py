from django.apps import AppConfig


class ProductConfig(AppConfig):
    verbose_name = "Продукты"
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product'

    def ready(self) -> None:
        from product.utils import signals
