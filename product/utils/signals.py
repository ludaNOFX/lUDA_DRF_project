from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from product.models.product import Product


# Обработчик для обновления количества продуктов у производителя при сохранении или удалении связи
@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def update_product_count(sender: Product, instance: Product, **kwargs: dict) -> None:
    if instance.manufacturer:
        manufacturer = instance.manufacturer
        manufacturer.product_count = manufacturer.products.count()
        manufacturer.save()
