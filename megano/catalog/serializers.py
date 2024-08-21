
from rest_framework import serializers

from product.models import Category


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category

    def to_representation(self, obj):
        all_cat = Category.objects.all()

        def search_subcategories(parent_cat_id: int) -> list:
            """
            Функция search_subcategories возвращает список с вложенными словарями, в словарях данные о
            категориях и подкатегориях товаров.
            Функция проверяет наличие дочерних категорий у родительской категории,
            при наличии дочерней категории, она добавляется в родительскую подкатегорию
            """

            # создаём список для хранения данных подкатегорий
            cat_list = []

            # из таблицы с категориями товаров по id родительской категории получаем список (QuerySet)
            # с возможными подкатегориями
            list_parent_cat_obj = all_cat.filter(parent_category=parent_cat_id)

            # если полученный список с подкатегориями не пустой
            if list_parent_cat_obj:
                # переберём его
                for cat in list_parent_cat_obj:
                    # каждую подкатегорию добавим в ранее созданный список cat_list
                    cat_list.append(
                        {
                            "pk": cat.pk,
                            "title": cat.title,
                            "image": {
                                "src": str(cat.image.url),
                                "alt": cat.title,
                            },
                            # для каждой подкатегории вызываем функцию поиска подкатегории
                            "subcategories": search_subcategories(parent_cat_id=cat.pk),
                        }
                    )
                return cat_list
            return cat_list

        # возвращается результат главной функции to_representation
        return {
                "pk": obj.pk,
                "title": obj.title,
                "image": {
                    "src": str(obj.image.url),
                    "alt": obj.title,
                },
                "subcategories": search_subcategories(parent_cat_id=obj.pk),
            }
