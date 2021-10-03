from django.contrib import admin

from .models import Favorite, Ingredient, Recipe, Recipeingredient, ShoppingCart, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """ Регестируем модель рецептов"""

    list_display = ('author', 'name', 'number_of_favorites')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'

    def number_of_favorites(self, obj):
        return obj.favorites.all().count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """ Регестируем модель ингридиентов"""

    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """ Регестируем модель тегов"""

    list_display = ('title', 'slug', 'color')
    list_filter = ('title',)
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """ Регестируем модель избранного"""

    list_display = ('user', 'recipe')
    list_filter = ('user',)
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """ Регестируем модель списка покупок"""

    list_display = ('user', 'recipe')
    list_filter = ('user',)
    empty_value_display = '-пусто-'


@admin.register(Recipeingredient)
class RecipeingredientAdmin(admin.ModelAdmin):
    """ Регестируем модель рецептов"""

    list_display = ('ingredient', 'recipe', 'amount')
    list_filter = ('ingredient', 'recipe')
    empty_value_display = '-пусто-'
