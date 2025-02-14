from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from recipeapp.forms import UserBioForm, IngredientForm, RecipeForm, IngredientSelectionForm
from recipeapp.models import Ingredient, Recipe, Category


class RecipeFilterMixin:
    """Миксин для фильтрации и поиска рецептов."""

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтрация по категории (если передана в URL)
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(categories__id=category_id)

        # Поиск по названию (если передан в URL)
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Добавляем список категорий для фильтрации
        context['categories'] = Category.objects.all()

        # Также можно добавить дополнительные данные, если нужно
        # например, передать общее количество рецептов для отображения на странице
        context['total_recipes'] = self.get_queryset().count()

        return context


class RecipeIndexView(RecipeFilterMixin, ListView):
    model = Recipe
    template_name = 'recipeapp/recipe/recipe-index.html'
    context_object_name = 'recipes'
    paginate_by = 10


class IngredientDetailsView(DetailView):
    template_name = 'recipeapp/ingredient/ingredient-details.html'
    context_object_name = 'ingredient'

    def get_queryset(self):
        return Ingredient.objects.filter(archived=False)


class IngredientListView(ListView):
    template_name = 'recipeapp/ingredient/ingredient-list.html'
    context_object_name = 'ingredients'
    queryset = Ingredient.objects.filter(archived=False)
    paginate_by = 10  # Пагинация по 10 ингредиентов на странице


class IngredientCreateView(CreateView):
    model = Ingredient
    fields = 'name', 'description', 'measure'
    success_url = reverse_lazy('recipeapp:ingredient_list')


class IngredientUpdateView(UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('recipeapp:ingredient_details', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        # Обработка загрузки изображений
        # files = form.cleaned_data['images']
        # for image in files:
        #     IngredientImage.objects.create(product=self.object, image=image)
        return response


class IngredientDeleteView(DeleteView):
    model = Ingredient
    success_url = reverse_lazy('recipeapp:ingredient_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class RecipeListView(RecipeFilterMixin, ListView):
    model = Recipe
    template_name = 'recipeapp/recipe/recipe-list.html'
    context_object_name = 'recipes'
    paginate_by = 10


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipeapp/recipe/recipe-detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем средний рейтинг рецепта
        context['average_rating'] = self.object.average_rating()
        return context


def user_form(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserBioForm(request.POST)
        if form.is_valid():
            # Обработка данных формы
            bio = form.cleaned_data['bio']
            request.user.profile.bio = bio
            request.user.profile.save()
            return redirect('recipe:index')
    else:
        form = UserBioForm()
    context = {'form': form}
    return render(request, 'recipeapp/user-bio-form.html', context=context)


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = 'recipeapp/recipe/recipe-create.html'
    fields = ['name', 'description', 'instructions', 'cooking_time', 'image', 'ingredients', 'categories']
    success_url = reverse_lazy('recipeapp:recipe_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipeapp/recipe/recipe-update.html'
    success_url = reverse_lazy('recipeapp:recipe_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем все неархивированные ингредиенты
        ingredients = Ingredient.objects.filter(archived=False)
        # Создаем словарь с количеством ингредиентов для текущего рецепта
        ingredient_quantities = {
            ingredient.id: self.object.recipe_ingredients.filter(ingredient=ingredient).first().quantity
            if self.object.recipe_ingredients.filter(ingredient=ingredient).exists()
            else 1
            for ingredient in ingredients
        }
        context['ingredients'] = ingredients
        context['ingredient_quantities'] = ingredient_quantities
        return context


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipeapp:recipe_index')


class CategoryListView(ListView):
    model = Category
    template_name = 'recipeapp/category/category_list.html'
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'recipeapp/category/category_detail.html'
    context_object_name = 'category'


class CategoryCreateView(CreateView):
    model = Category
    template_name = 'recipeapp/category/category_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('category_list')


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'recipeapp/category/category_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('category_list')


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'recipeapp/category/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')

