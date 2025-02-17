from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .admin_mixins import ExportAsCSVMixin
from .models import Recipe, Ingredient, Category, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1  # Количество пустых форм для добавления ингредиентов


@admin.action(description='Archive Recipe')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Unarchive Recipe')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'measure', 'archived')
    list_display_links = ('pk', 'name')
    ordering = ('name',)
    search_fields = ('name', 'description')
    list_filter = ('archived',)
    actions = [mark_archived, mark_unarchived]

    fieldsets = [
        (None, {
            'fields': ('name', 'description', 'measure')
        }),
        ('Extra options', {
            'fields': ('archived',),
            'classes': ('collapse',),
            'description': 'Поле для переноса записи в архив',
        })
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description')
    list_display_links = ('pk', 'name')
    search_fields = ('name', 'description')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = ['mark_archived', 'mark_unarchived', 'export_csv']
    inlines = [RecipeIngredientInline]
    list_display = ('pk', 'name', 'description_short', 'categories_list', 'rate', 'created_by_verbose', 'archived')
    list_display_links = ('pk', 'name')
    ordering = ('-rate',)
    search_fields = ('name', 'description')
    list_filter = ('archived', 'categories', 'created_by')
    fieldsets = [
        (None, {
            'fields': ('name', 'description', 'instructions', 'cooking_time', 'image')
        }),
        ('Ingredients', {
            'fields': ('categories',),
            'classes': ('collapse', 'wide')
        }),
        ('Extra options', {
            'fields': ('archived',),
            'classes': ('collapse',),
            'description': 'Поле для переноса записи в архив',
        })
    ]

    def description_short(self, obj: Recipe) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + '...'

    def categories_list(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    categories_list.short_description = 'Categories'

    def get_queryset(self, request):
        return Recipe.objects.select_related('created_by').prefetch_related('recipe_ingredients__ingredient', 'categories')

    def created_by_verbose(self, obj: Recipe) -> str:
        return obj.created_by.first_name or obj.created_by.username