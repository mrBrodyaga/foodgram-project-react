from rest_framework import serializers

from .models import Tag, Recipe, Ingredient, Favorite, Recipeingredient, ShoppingCart


class TagSerializer(serializers.ModelSerializer):
    """ Сериализуем Теги"""

    class Meta:
        fields = '__all__'
        model = Tag


class RecipeSerializer(serializers.ModelSerializer):
    """ Сериализуем рецепты"""
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        fields = '__all__'
        model = Recipe
        depth = 2


class IngredientSerializer(serializers.ModelSerializer):
    """ Сериализуем ингридиенты"""

    class Meta:
        fields = '__all__'
        model = Ingredient


class FavoriteSerializer(serializers.ModelSerializer):
    """ Сериализуем избранное"""

    class Meta:
        fields = '__all__'
        model = Favorite


class ShoppingCartSerializer(serializers.ModelSerializer):
    """ Сериализуем список покупок"""

    class Meta:
        fields = '__all__'
        model = ShoppingCart
