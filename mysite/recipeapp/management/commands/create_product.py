from django.core.management import BaseCommand
from recipeapp.models import Ingredient, Category


class Command(BaseCommand):
    """
    Создает новые ингредиенты и категории.
    """
    help = "Создает базовые ингредиенты и категории для проекта."

    def handle(self, *args, **options):
        self.stdout.write('Создание новых ингредиентов и категорий')

        # Создаем категории, если они используются
        categories = [
            ('Горячее', 'Горячие блюда'),
            ('Суп', 'Супы'),
            ('Салат', 'Салаты'),
            ('Десерт', 'Десерты'),
        ]

        for name, description in categories:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            if created:
                self.stdout.write(f'Создана категория - {category.name}')
            else:
                self.stdout.write(f'Категория уже существует - {category.name}')

        # Создаем ингредиенты
        ingredients = [
            ('Говядина', 'филейная часть', 'г'),
            ('Картофель', '', 'шт'),
            ('Перец болгарский', '', 'шт'),
            ('Морковь', '', 'шт'),
            ('Помидоры', '', 'шт'),
            ('Помидоры', 'черри', 'шт'),
            ('Лук', 'репчатый', 'шт'),
            ('Лук', 'зеленый', 'шт'),
            ('Чеснок', '', 'зубчик(а)'),
            ('Томатная паста', '', 'г'),
            ('Паприка', '', 'г'),
            ('Тмин', '', 'г'),
            ('Масло', 'подсолнечное', 'г'),
            ('Масло', 'сливочное', 'г'),
            ('Креветки', '', 'г'),
            ('Авокадо', '', 'шт'),
            ('Руккола', '', 'г'),
            ('Сыр', '', 'г'),
            ('Лимон', '', 'шт'),
        ]

        for name, description, measure in ingredients:
            ingredient, created = Ingredient.objects.get_or_create(
                name=name,
                defaults={'description': description, 'measure': measure}
            )
            if created:
                self.stdout.write(f'Создан новый ингредиент - {ingredient.name}')
            else:
                self.stdout.write(f'Ингредиент уже существует - {ingredient.name}')

        self.stdout.write(self.style.SUCCESS('Успешно созданы ингредиенты и категории'))