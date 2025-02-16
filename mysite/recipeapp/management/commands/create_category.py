from django.core.management import BaseCommand
from recipeapp.models import Category


class Command(BaseCommand):
    """
    Создает базовые категории для проекта.
    """
    help = "Создает базовые категории для проекта."

    def handle(self, *args, **options):
        self.stdout.write('Создание новых категорий')

        # Список категорий для создания
        categories = [
            ('Горячее', 'Горячие блюда'),
            ('Суп', 'Супы'),
            ('Салат', 'Салаты'),
            ('Десерт', 'Десерты'),
            ('Закуска', 'Закуски'),
            ('Напиток', 'Напитки'),
            ('Выпечка', 'Выпечка и хлеб'),
        ]

        # Создаем категории
        for name, description in categories:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            if created:
                self.stdout.write(f'Создана категория - {category.name}')
            else:
                self.stdout.write(f'Категория уже существует - {category.name}')

        self.stdout.write(self.style.SUCCESS('Успешно созданы категории'))