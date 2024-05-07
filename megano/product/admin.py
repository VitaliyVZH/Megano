
from django.contrib import admin
from django.db.models import Avg
from django.utils.safestring import mark_safe

from product.models import Product, Category, Reviews, Specifications, ProductImage, Tag


class ReviewsProductInline(admin.TabularInline):
    """
    Класс ReviewsProductInline добавляется в класс ProductAdmin, что позволяет отображать связанные
    с товаром отзывы
    """

    model = Reviews
    # extra устанавливает кол-во дополнительных пустых форм, которые необходимы для заполнения
    extra = 1


class SpecificationsInline(admin.TabularInline):
    """
    Класс SpecificationsInline добавляется в класс ProductAdmin, что позволяет отображать связанную
    с товаром спецификацию
    """

    model = Specifications


class ImageProductInline(admin.TabularInline):
    model = ProductImage

    fields = "alt", "src",
    extra = 0

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.avatar.src.url}>')


class TagProductInline(admin.TabularInline):
    model = Tag.products.through
    list_display = "pk", "name"

    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Класс ProductAdmin реализует в админ панели доступ к товарам, отзывам о товарах и спецификации товара"""

    # list_select_related = ('author', 'category') попробовать

    # перечень моделей, которые отображаются в админ панели Товаров
    inlines = [
        SpecificationsInline,
        ReviewsProductInline,
        ImageProductInline,
        TagProductInline,
    ]

    # отображаемые поля модели Product в общем списке
    list_display = [
        "pk",
        "price",
        "category",
        "count",
        "date",
        "title",
        "description",
        "short_full_desc",
        "freeDelivery",
        "average_product_rating",
        "preview"

    ]

    list_display_links = "pk", "title", "category",  "preview"
    ordering = "pk",

    # поля, которые отображаются в карточке товара
    fields = [
        "title",
        "price",
        "count",
        "category",
        "description",
        "fullDescription",
        "freeDelivery",
        "preview"
    ]

    readonly_fields = ["preview"]

    # date_hierarchy добавляет навигацию по дате в админ панели товаров
    date_hierarchy = "date"

    # list_filter добавляет блок фильтров в админ панели продуктов
    list_filter = "category", "title"

    # кол-во товаров отображенных на вкладке Products
    list_per_page = 20

    def short_full_desc(self, obj: Product) -> str:
        if obj.fullDescription and len(obj.fullDescription) > 50:
            return "".join([obj.fullDescription[:50], "..."])
        return obj.fullDescription

    def preview(self, obj):
        """
        При наличии фотографии, функция возвращает HTML код, что позволяет отобразить не путь к фото,
        а саму фотографию.
        """

        path = obj.images.get(product=obj).src
        if path:
            return mark_safe(f'<img src="{path.url}" width="60" height="60"')
        else:
            return "Нет фото"

    def average_product_rating(self, obj: Product):
        """Функция возвращает средний рейтинг товара"""

        average_rating = Reviews.objects.filter(product=obj).aggregate(Avg("rate"))["rate__avg"]
        if average_rating:
            return round(average_rating, 1)
        return 0.0


class ProductsInline(admin.TabularInline):
    """
    ProductsInline добавляется в список inlines класса CategoryAdmin для отображения в админ панели,
    в КАТЕГОРИЯХ связанных с этими категоряими товаров.
    """

    model = Product
    extra = 0  # кол-во форм для создания нового товара


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Класс CategoryAdmin реализует в админ панели КАТЕГОРИИ товаров."""

    inlines = [
        ProductsInline,
    ]

    list_display = "pk", "title", "preview"
    list_display_links = "pk", "title"
    ordering = "pk",
    readonly_fields = ["preview"]

    def preview(self, obj):
        """
        При наличии фотографии, функция возвращает HTML код, что позволяет отобразить не путь к фото,
        а саму фотографию.
        """

        if obj.image != "1":
            return mark_safe(f'<img src={obj.image.url} width="60" height="60"')
        else:
            return "Нет фото"


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    """Класс ReviewsAdmin реализует в админ панели доступ к отзывам о товарах"""

    list_display = "pk", "product", "author", "review", "rate", "date",

    # list_per_page устанавливает кол-во отображаемых отзывов в админ панели
    list_per_page = 20

    def review(self, obj):
        if obj.text and len(obj.text) > 50:
            return "".join([obj.text[:50], "..."])
        return obj.text


class TagProductsInline(admin.TabularInline):
    model = Tag.products.through
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    inlines = [
        TagProductsInline,
    ]

    list_display = "pk", "name",
    list_display_links = "pk", "name"
