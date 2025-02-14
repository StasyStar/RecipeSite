from django.core.management import BaseCommand
from recipeapp.models import Recipe, Ingredient, Category


class Command(BaseCommand):
    """
    Обновляет рецепт, добавляя ингредиенты и категории.
    """
    help = "Обновляет рецепт, добавляя ингредиенты и категории."

    def handle(self, *args, **options):
        self.stdout.write('Обновление рецепта')

        # Получаем первый рецепт
        recipe = Recipe.objects.first()
        if not recipe:
            self.stdout.write(self.style.ERROR('Рецепты не найдены'))
            return

        # Получаем все ингредиенты
        ingredients = Ingredient.objects.all()
        if not ingredients:
            self.stdout.write(self.style.ERROR('Ингредиенты не найдены'))
            return

        # Получаем категорию
        category, created = Category.objects.get_or_create(name='Горячее')
        if created:
            self.stdout.write(f'Создана категория - {category.name}')
        else:
            self.stdout.write(f'Категория уже существует - {category.name}')

        # Добавляем ингредиенты и категории
        recipe.ingredients.set(ingredients)
        recipe.categories.add(category)
        recipe.save()

        self.stdout.write(self.style.SUCCESS(f'Успешно обновлен рецепт "{recipe.name}"'))