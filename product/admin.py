from typing import List, Tuple
from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.safestring import mark_safe
from django.utils.safestring import SafeString
from product.models.category import Category
from product.models.detail import ProductDetail
from product.models.manufacturer import Manufacturer
from product.models.product import Product
from product.models.tagproduct import TagProduct


class DetailedFilter(admin.SimpleListFilter):
    title = "Детали у продукта"
    parameter_name = 'detail'

    def lookups(self, request: HttpRequest, model_admin) -> List[Tuple[str, str]]:
        return [
            ('detailed', 'Есть детали о продукте'),
            ('not_detailed', 'Нет деталей о продукте'),
        ]

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet:
        if self.value() == 'detailed':
            return queryset.filter(detail__isnull=False)
        elif self.value() == 'not_detailed':
            return queryset.filter(detail__isnull=True)
        else:
            return queryset


class ProductDetailInline(admin.StackedInline):
    model = ProductDetail
    can_delete = False
    readonly_fields = ['slug']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'user',
        'slug',
        'product_image',
        'image',
        'description',
        'is_published',
        'price',
        'quantity',
        'cat',
        'tags',
        'manufacturer',
    ]
    readonly_fields = ['slug', 'product_image']
    list_display = ('name', 'user', 'product_image', 'price', 'quantity', 'time_create', 'is_published', 'cat')
    list_display_links = ('name', )
    ordering = ('-time_create', 'name')
    list_editable = ('is_published', )
    list_per_page = 5
    actions = ('set_published', 'set_draft')
    search_fields = ['name', 'cat__name']
    list_filter = [DetailedFilter, 'cat__name', 'is_published']
    filter_horizontal = ['tags']
    inlines = [ProductDetailInline]  # Добавляем встроенную форму для ProductDetail
    save_on_top = True

    @admin.display(description='Демонстрация изображения')
    def product_image(self, product: Product) -> SafeString | str:
        if product.image:
            return mark_safe(f"<img src='{product.image.url}' width=50>")
        return "Без изображения"

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request: HttpRequest, queryset: QuerySet) -> None:
        count = queryset.update(is_published=Product.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count}")

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request: HttpRequest, queryset: QuerySet) -> None:
        count = queryset.update(is_published=Product.Status.DRAFT)
        self.message_user(request, f"{count} сняты с публикации!", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    readonly_fields = ['slug']


@admin.register(TagProduct)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag')
    list_display_links = ('id', 'tag')
    readonly_fields = ['slug']


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'website', 'product_count')
    list_display_links = ('id', 'name', 'address', 'website', 'product_count')
    readonly_fields = ['slug']


admin.site.register(ProductDetail)  # Регистрация модели ProductDetail отдельно
