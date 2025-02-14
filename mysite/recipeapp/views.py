from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from recipeapp.forms import UserBioForm, IngredientForm, RecipeForm, RecipeIngredient
from recipeapp.models import Ingredient, Recipe, Category, Comment, Rating


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
    template_name = 'recipeapp/ingredient/ingredient-list.html'  # Путь к шаблону
    context_object_name = 'ingredients'  # Имя переменной контекста
    paginate_by = 10  # Пагинация по 10 ингредиентов на странице

    def get_queryset(self):
        # Получаем параметр сортировки из запроса (например, ?sort=name)
        sort_by = self.request.GET.get('sort', 'name')  # По умолчанию сортируем по имени

        # Определяем допустимые поля для сортировки
        valid_sort_fields = ['name', 'measure', '-name', '-measure']
        if sort_by not in valid_sort_fields:
            sort_by = 'name'  # Если поле сортировки недопустимо, сортируем по умолчанию

        # Возвращаем отсортированный и отфильтрованный queryset
        return Ingredient.objects.filter(archived=False).order_by(sort_by)

    def get_context_data(self, **kwargs):
        # Добавляем параметр сортировки в контекст
        context = super().get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort', 'name')  # Передаем текущую сортировку в шаблон
        return context


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


class IngredientDeleteView(View):
    success_url = reverse_lazy('recipeapp:ingredient_list')

    def post(self, request, *args, **kwargs):
        # Получаем список выбранных ингредиентов
        ingredient_ids = request.POST.getlist('ingredient_ids')

        if ingredient_ids:
            # Архивируем выбранные ингредиенты
            Ingredient.objects.filter(id__in=ingredient_ids).update(archived=True)
            messages.success(request, 'Выбранные ингредиенты успешно архивированы.')
        else:
            messages.error(request, 'Не выбрано ни одного ингредиента для архивирования.')

        # Перенаправляем на страницу списка ингредиентов
        return HttpResponseRedirect(self.success_url)


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


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipeapp/recipe/recipe-create.html'
    success_url = reverse_lazy('recipeapp:recipe_index')  # Перенаправление на список рецептов

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем все неархивированные ингредиенты
        context['ingredients'] = Ingredient.objects.filter(archived=False)
        return context

    def form_valid(self, form):
        # Сохраняем рецепт
        recipe = form.save(commit=False)
        recipe.created_by = self.request.user
        recipe.save()

        # Обрабатываем ингредиенты
        ingredients = Ingredient.objects.filter(archived=False)
        for ingredient in ingredients:
            ingredient_id = ingredient.id
            is_selected = self.request.POST.get(f'ingredient_{ingredient_id}') == 'on'
            quantity = self.request.POST.get(f'quantity_{ingredient_id}', 1)

            if is_selected:
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=quantity
                )

        return super().form_valid(form)


class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipeapp/recipe/recipe-update.html'

    def get_success_url(self):
        # Редирект на страницу с деталями текущего рецепта
        return reverse_lazy('recipeapp:recipe_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ingredients = Ingredient.objects.filter(archived=False)
        ingredient_quantities = {
            ingredient.id: self.object.recipe_ingredients.filter(ingredient=ingredient).first().quantity
            if self.object.recipe_ingredients.filter(ingredient=ingredient).exists()
            else 1
            for ingredient in ingredients
        }
        context['ingredients'] = ingredients
        context['ingredient_quantities'] = ingredient_quantities
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            # Сохраняем основную форму
            self.object = form.save()

            # Обрабатываем ингредиенты
            ingredients = Ingredient.objects.filter(archived=False)
            for ingredient in ingredients:
                ingredient_id = ingredient.id
                is_selected = request.POST.get(f'ingredient_{ingredient_id}') == 'on'
                quantity = request.POST.get(f'quantity_{ingredient_id}', 1)

                if is_selected:
                    RecipeIngredient.objects.update_or_create(
                        recipe=self.object,
                        ingredient=ingredient,
                        defaults={'quantity': quantity}
                    )
                else:
                    RecipeIngredient.objects.filter(recipe=self.object, ingredient=ingredient).delete()

            # Вызываем form_valid для выполнения редиректа
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


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


@login_required
def add_comment(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        text = request.POST.get('text')
        Comment.objects.create(recipe=recipe, user=request.user, text=text)
    return redirect('recipeapp:recipe_detail', pk=pk)


@login_required
def rate_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 0))
        Rating.objects.update_or_create(
            recipe=recipe,
            user=request.user,
            defaults={'value': rating}
        )
    return redirect('recipeapp:recipe_detail', pk=pk)

