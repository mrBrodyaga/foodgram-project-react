from django.contrib import admin
from .models import Recipe, Favorite, Ingredient, Recipeingredient, Tag

#! Вывести все модели с возможностью редактирования и удаление записей

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """ Регестируем модель рецептов"""

    list_display = ('author', 'name', ) # 'number_of_favorites'
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'
# #! На странице рецепта вывести общее число добавлений этого рецепта в избранное.
#     @admin.display(empty_value=None)
#     def number_of_favorites(self, obj):
#         return obj.is_favorite.all().count() #! не пойму что после obj

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