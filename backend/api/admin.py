from django.contrib import admin
from .models import Recipe, Favorite, Ingredient, Recipeingredient, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """ Регестируем модель рецептов"""

    list_display = ('author', 'name')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'
# На странице рецепта вывести общее число добавлений этого рецепта в избранное.

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """ Регестируем модель ингридиентов"""

    list_display = ('title', 'dimension')
    list_filter = ('title',)
    empty_value_display = '-пусто-'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """ Регестируем модель тегов"""

    list_display = ('title', 'slug', 'color')
    list_filter = ('title',)
    empty_value_display = '-пусто-'