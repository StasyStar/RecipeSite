from django.urls import path
from recipeapp import views

app_name = 'recipeapp'

urlpatterns = [
    # Главная страница
    path('', views.RecipeIndexView.as_view(), name='recipe_index'),

    # Рецепты
    path('recipes/', views.RecipeListView.as_view(), name='recipe_list'),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipes/create/', views.RecipeCreateView.as_view(), name='recipe_create'),
    path('recipes/<int:pk>/update/', views.RecipeUpdateView.as_view(), name='recipe_update'),
    path('recipes/<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='recipe_delete'),
    path('recipe/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('recipes/<int:pk>/rate/', views.rate_recipe, name='rate_recipe'),

    # Ингредиенты
    path('ingredients/', views.IngredientListView.as_view(), name='ingredient_list'),
    path('ingredients/<int:pk>/', views.IngredientDetailsView.as_view(), name='ingredient_detail'),
    path('ingredients/create/', views.IngredientCreateView.as_view(), name='ingredient_create'),
    path('ingredients/<int:pk>/update/', views.IngredientUpdateView.as_view(), name='ingredient_update'),
    path('ingredients/delete/', views.IngredientDeleteView.as_view(), name='ingredient_delete'),
]

