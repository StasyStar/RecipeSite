from django import forms
from recipeapp.models import Ingredient, Recipe, Category, RecipeIngredient


class UserBioForm(forms.Form):
    name = forms.CharField(max_length=100, label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    age = forms.IntegerField(label='Ваш возраст', min_value=1, max_value=110,
                             widget=forms.NumberInput(attrs={'class': 'form-control'}))
    bio = forms.CharField(label='Биография', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'description', 'measure']  # Указываем только существующие поля
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'measure': forms.TextInput(attrs={'class': 'form-control'}),
        }


class IngredientSelectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        ingredients = kwargs.pop('ingredients', None)
        super().__init__(*args, **kwargs)
        for ingredient in ingredients:
            self.fields[f'ingredient_{ingredient.id}'] = forms.BooleanField(
                required=False,
                label=ingredient.name,
                widget=forms.CheckboxInput()
            )
            self.fields[f'quantity_{ingredient.id}'] = forms.IntegerField(
                required=False,
                initial=1,
                min_value=1,
                label='Количество',
                widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 80px;'})
            )
            self.fields[f'measure_{ingredient.id}'] = forms.CharField(
                required=False,
                initial=ingredient.measure,
                label='Единица измерения',
                widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'style': 'width: 80px;'})
            )


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'instructions', 'cooking_time', 'image', 'categories']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'cooking_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем поля для ингредиентов
        self.ingredients = Ingredient.objects.filter(archived=False)
        for ingredient in self.ingredients:
            self.fields[f'ingredient_{ingredient.id}'] = forms.BooleanField(
                required=False,
                label=ingredient.name,
                widget=forms.CheckboxInput()
            )
            self.fields[f'quantity_{ingredient.id}'] = forms.IntegerField(
                required=False,
                initial=1,
                min_value=1,
                label='Количество',
                widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 80px;'})
            )

    def save(self, commit=True):
        recipe = super().save(commit=False)
        if commit:
            recipe.save()
        # Сохраняем ингредиенты
        for ingredient in self.ingredients:
            if self.cleaned_data.get(f'ingredient_{ingredient.id}'):
                quantity = self.cleaned_data.get(f'quantity_{ingredient.id}', 1)
                RecipeIngredient.objects.update_or_create(
                    recipe=recipe,
                    ingredient=ingredient,
                    defaults={'quantity': quantity}
                )
            else:
                RecipeIngredient.objects.filter(recipe=recipe, ingredient=ingredient).delete()
        return recipe


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
