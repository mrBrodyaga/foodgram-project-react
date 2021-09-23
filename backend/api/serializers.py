from rest_framework import serializers

from .models import Tag, Recipe, Ingredient, Favorite, Recipeingredient, ShoppingCart
from users.serializers import CustomUserSerializer
class TagSerializer(serializers.ModelSerializer):
    """ Сериализуем Теги"""

    class Meta:
        fields = '__all__'
        model = Tag


class RecipeSerializer(serializers.ModelSerializer):
    """ Сериализуем рецепты"""
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = CustomUserSerializer()

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        user = request.user

        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        user = request.user

        return Favorite.objects.filter(user=user, recipe=obj).exists()

    class Meta:
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')
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
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe


class ShoppingCartSerializer(serializers.ModelSerializer):
    """ Сериализуем список покупок"""

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe
