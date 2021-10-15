from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from users.serializers import CustomUserSerializer
from django.db import transaction
from .models import Favorite, Ingredient, Recipe, Tag, Recipeingredient
from drf_extra_fields.fields import Base64ImageField


class TagSerializer(serializers.ModelSerializer):
    """Сериализуем Теги"""

    class Meta:
        fields = "__all__"
        model = Tag



# class CreateRecipeIngredientSerializer(serializers.Serializer):
#     """Сериализуем ?"""
#     id = serializers.IntegerField(required=True)
#     amount = serializers.FloatField(required=True, min_value=1)

class CreateRecipeIngredientSerializer(serializers.Serializer):
    """Сериализуем инпидиенты для создания рецептов"""
    id = serializers.PrimaryKeyRelatedField(
            queryset=Ingredient.objects.all()
        )

    class Meta:
        model = Recipeingredient
        fields = ('id', 'amount')

class RecipeSerializer(serializers.ModelSerializer):
    """Сериализуем рецепты"""

    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    # image = Base64ImageField()
    # author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # def to_representation(self, instance):
    #     if self.context['request'].method != 'GET':
    #         serializer = RecipeCreateSerializer(instance)
    #         return serializer.data
    #     return super().to_representation(instance)

    # def create(self, validated_data):
    #     ingredients = validated_data.pop('ingredients')
    #     tags = validated_data.pop('tags')

    #     recipe = Recipe.objects.create(**validated_data)
    #     recipe.tags.set(tags)

    #     for ingredient_data in ingredients:
    #         ingredient_id = ingredient_data["id"]
    #         ingredient_amount = ingredient_data["amount"]

    #         Recipeingredient.objects.create(
    #             ingredient_id=ingredient_id,
    #             amount=ingredient_amount,
    #             recipe=recipe,
    #         )
    #     return recipe

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        user = request.user

        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        user = request.user

        return Favorite.objects.filter(user=user, recipe=obj).exists()

    class Meta:
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )
        model = Recipe
        # extra_kwargs = {
        #     "ingredients": {"write_only": True},
        # }
        depth = 2

# class RecipeCreateSerializer(serializers.Serializer):
#     """Сериализуем рецепты для создания"""
#     name = serializers.CharField(required=True)
#     text = serializers.CharField(required=True)
#     cooking_time = serializers.IntegerField(required=True, min_value=1)
#     tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
#     ingredients = CreateRecipeIngredientSerializer(many=True)

#     author = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     image = Base64ImageField()

#     class Meta:
#         model = Recipe
#         fields = (
#             "name",
#             "text",
#             "cooking_time",
#             "tags",
#             "ingredients",
#             "author",
#             "image",
#         )

#         depth = 2

#     def create(self, validated_data):
#         ingredients = validated_data.pop('ingredients')
#         tags = validated_data.pop('tags')

#         recipe = Recipe.objects.create(**validated_data)
#         recipe.tags.set(tags)

#         for ingredient_data in ingredients:
#             ingredient_id = ingredient_data["id"]
#             ingredient_amount = ingredient_data["amount"]

#             Recipeingredient.objects.create(
#                 ingredient_id=ingredient_id,
#                 amount=ingredient_amount,
#                 recipe=recipe,
#             )
#         return recipe

class RecipeCreateSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    ingredients = Recipeingredient(
        many=True, source='ingredient_amount')
    image = Base64ImageField()


    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'ingredients', 'name', 'image', 'text', 'cooking_time')


    def validate(self, data):
        if data['cooking_time'] <= 0:
            raise serializers.ValidationError(
                'Нереально так быстро приготовить')
        if Recipe.objects.filter(name=data['name']) and (
                self.context['request'].method == 'POST'):
            raise serializers.ValidationError(
                'Рецепт с таким именем уже есть!')
        return data

    def validate_ingredients(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_set = set()
        if not ingredients:
            raise serializers.ValidationError(
                'Добавьте хотя бы один ингредиент')
        for ingredient in ingredients:
            if int(ingredient['amount']) < 1:
                raise serializers.ValidationError(
                    'Количество ингредиента не может быть меньше 1.')
            ingredient_id = ingredient.get('id')
            if ingredient_id in ingredients_set:
                raise serializers.ValidationError(
                    'Ингредиент в списке должен быть уникальным.'
                )
            ingredients_set.add(ingredient_id)
        return data

    def validate_tags(self, data):
        tags_set = set()
        if not data:
            raise serializers.ValidationError(
                'Добавьте хотя бы один тэг')
        for tag in data:
            if tag in tags_set:
                raise serializers.ValidationError(
                    'Ингредиент в списке должен быть уникальным.'
                )
            tags_set.add(tag)
        return data

    def ingredient_add(self, ingredients, recipe):
        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(
                id=ingredient['id'].id)
            Recipeingredient.objects.create(
                ingredients=current_ingredient,
                recipes=recipe,
                amount=ingredient['amount'])
        return recipe

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredient_amount')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        recipe = self.ingredient_add(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredient_amount')
        instance.name = validated_data['name']
        instance.text = validated_data['text']
        instance.image = validated_data['image']
        instance.cooking_time = validated_data['cooking_time']
        instance.tags.set(tags)
        instance = self.ingredient_add(ingredients, instance)
        instance.save()
        return instance

class IngredientSerializer(serializers.ModelSerializer):
    """Сериализуем ингридиенты"""

    class Meta:
        fields = "__all__"
        model = Ingredient


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализуем избранное"""

    class Meta:
        fields = ("id", "name", "image", "cooking_time")
        model = Recipe


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализуем список покупок"""

    class Meta:
        fields = ("id", "name", "image", "cooking_time")
        model = Recipe
