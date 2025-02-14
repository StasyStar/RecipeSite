from django.contrib.auth.models import User
from django.core.management import BaseCommand
from recipeapp.models import Recipe, Ingredient, Category


class Command(BaseCommand):
    """
    Создает новый рецепт.
    """
    help = "Создает тестовый рецепт для проекта."

    def handle(self, *args, **options):
        self.stdout.write('Создание нового рецепта')

        # Получаем или создаем пользователя
        user, created = User.objects.get_or_create(
            username='stasy',
            defaults={'first_name': 'Stasy', 'email': 'stasy@example.com'}
        )
        if created:
            self.stdout.write(f'Создан новый пользователь - {user.username}')
        else:
            self.stdout.write(f'Пользователь уже существует - {user.username}')

        # Получаем ингредиенты
        ingredients = Ingredient.objects.filter(name__in=['Говядина', 'Картофель', 'Лук', 'Чеснок', 'Томатная паста'])
        if not ingredients:
            self.stdout.write(self.style.ERROR('Ингредиенты не найдены'))
            return

        # Получаем категорию
        category, created = Category.objects.get_or_create(name='Горячее')
        if created:
            self.stdout.write(f'Создана категория - {category.name}')
        else:
            self.stdout.write(f'Категория уже существует - {category.name}')

        # Создаем рецепт
        recipe, created = Recipe.objects.get_or_create(
            name='Венгерский суп-гуляш',
            defaults={
                'description': 'Венгерский суп-гуляш из говядины - отличный вариант для обеда. Суп-гуляш по этому '
                               'рецепту очень сытный и ароматный.',
                'instructions': '1. Готовим ингредиенты. '
                                '2. Обжариваем лук и добавляем томатную пасту, чеснок, паприку и тмин.'
                                '3. Нарезаем мясо и добавляем к луку, наливаем стакан воды и томим 1 час. '
                                '4. Добавляем перец, морковь, помидоры и картофель к мясу. '
                                '5. Солим, добавляем еще 3 стакана воды и томим еще полчаса.',
                'meal_type': 'горячее',
                'cooking_time': 90,  # Добавлено время приготовления (в минутах)
                'created_by': user,
            }
        )

        # Добавляем ингредиенты и категории
        recipe.ingredients.set(ingredients)
        recipe.categories.add(category)
        recipe.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Рецепт "{recipe.name}" успешно создан.'))
        else:
            self.stdout.write(f'Рецепт уже существует - {recipe.name}')
