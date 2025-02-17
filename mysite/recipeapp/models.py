from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'  # Название модели в единственном числе
        verbose_name_plural = 'Ингредиенты'  # Название модели во множественном числе

    name = models.CharField(
        max_length=200,
        null=False,
        verbose_name="Название"  # Название поля
    )
    description = models.TextField(
        null=False,
        blank=True,
        db_index=True,
        verbose_name="Описание"  # Название поля
    )
    measure = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Единица измерения"  # Название поля
    )
    archived = models.BooleanField(
        default=False,
        verbose_name="Архивировано"  # Название поля
    )

    def __str__(self) -> str:
        return f'Продукт(название={self.name}, описание={self.description}, мера={self.measure})'


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    instructions = models.TextField()
    cooking_time = models.PositiveIntegerField(help_text="Время приготовления в минутах")
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    meal_type = models.CharField(max_length=50, choices=[
        ('hot', 'Горячее'),
        ('soup', 'Суп'),
        ('salad', 'Салат'),
        ('dessert', 'Десерт'),
    ], default='hot')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category', related_name='recipes')
    archived = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Recipe(№={self.pk}, name={self.name!r}, description={self.description!r})'

    # Метод для расчета среднего рейтинга
    def average_rating(self):
        from django.db.models import Avg
        return self.ratings.aggregate(Avg('value'))['value__avg'] or 0


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='recipe_ingredients')
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.ingredient.name} ({self.quantity} {self.ingredient.measure}) в рецепте {self.recipe.name}'


class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'Comment by {self.user.username} on {self.recipe.name}'


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    value = models.IntegerField()

    class Meta:
        unique_together = ('user', 'recipe')  # Один пользователь может оставить только одну оценку на рецепт

    def __str__(self):
        return f'Rating {self.value} by {self.user.username} on {self.recipe.name}'
