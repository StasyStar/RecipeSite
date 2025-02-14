from django import forms
from recipeapp.models import Ingredient, Recipe, Category


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
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'instructions': 'Инструкции',
            'cooking_time': 'Время приготовления (мин)',
            'image': 'Изображение',
            'categories': 'Категории',
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
