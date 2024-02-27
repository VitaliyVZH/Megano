
from django.contrib import admin
from django.db.models import Avg
from django.utils.safestring import mark_safe

from product.models import Product, Category, Reviews, Specifications, ProductImage


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
    extra = 1

    def get_image(self, obj):
        # if not obj.avatar.src:
        #     return f"No image"
        return mark_safe(f'<img src={obj.avatar.src.url}>')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Класс ProductAdmin реализует в админ панели доступ к товарам, отзывам о товарах и спецификации товара"""

    # list_select_related = ('author', 'category') попробовать

    # перечень моделей, которые отображаются в админ панели Товаров
    inlines = [
        SpecificationsInline,
        ReviewsProductInline,
        ImageProductInline,
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
        "fullDescription",
        "freeDelivery",
        "avg_products_rating",

    ]

    list_display_links = "pk", "title"
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
    ]

    # date_hierarchy добавляет навигацию по дате в админ панели товаров
    date_hierarchy = "date"

    # list_filter добавляет блок фильтров в админ панели продуктов
    list_filter = "category", "title"

    # кол-во товаров отображенных на вкладке Products
    list_per_page = 20


    def avg_products_rating(self, obj: Product):
        """Функция возвращает средний рейтинг товара"""

        average_rating = Reviews.objects.filter(product=obj).aggregate(Avg("rate"))["rate__avg"]
        if average_rating:
            return round(average_rating, 1)
        return 0.0


class ProductsInline(admin.TabularInline):
    model = Product

    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        ProductsInline,
    ]
    list_display = "pk", "name",
    list_display_links = "pk", "name",


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    """Класс ReviewsAdmin реализует в админ панели доступ к отзывам о товарах"""

    list_display = "product", "author", "text", "rate", "date",

    # list_per_page устанавливает кол-во отображаемых отзывов в админ панели
    list_per_page = 20
