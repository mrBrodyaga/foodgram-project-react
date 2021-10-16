from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.serializers import CustomUserSerializer

from .models import (
    Favorite,
    Ingredient,
    Recipe,
    Recipeingredient,
    ShoppingCart,
    Tag,
)


class TagSerializer(serializers.ModelSerializer):
    """Сериализуем Теги"""

    class Meta:
        fields = "__all__"
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализуем ингридиенты"""

    class Meta:
        fields = "__all__"
        model = Ingredient

    def to_internal_value(self, data):
        try:
            ingredient = Ingredient.objects.get(id=data) # noqa: R504
        except Ingredient.DoesNotExist:
            raise serializers.ValidationError(
                {f"Ингредиента с id={data} не существует."}
            )
        return ingredient # noqa: R504


class RecipeIngredientsDetailsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="ingredient.id")

    class Meta:
        model = Recipeingredient
        fields = ("id", "amount")


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализуем рецепты"""

    author = CustomUserSerializer()
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        user = request.user

        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        user = request.user

        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()

    def get_ingredients(self, obj):
        ingredients = Recipeingredient.objects.filter(recipe=obj)
        data = []
        for item in ingredients:
            data.append(
                {
                    "id": item.ingredient.id,
                    "name": item.ingredient.name,
                    "measurement_unit": item.ingredient.measurement_unit,
                    "amount": item.amount,
                }
            )
        return data

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
        depth = 2


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientsDetailsSerializer(many=True)

    image = Base64ImageField(max_length=None, use_url=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Recipe
        exclude = ("pub_date",)

    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception=False)
        if not is_valid:
            errors = self.errors.copy()
            if "ingredients" in errors:
                ingredient_errors = errors["ingredients"]
                new_ingredient_errors = []
                for error in ingredient_errors:
                    if error != {}:
                        for key, values in error.items():
                            for value in values:
                                new_ingredient_errors.append(
                                    f"'{key}': {value}"
                                )
                errors["ingredients"] = new_ingredient_errors
            raise serializers.ValidationError(errors)
        return is_valid

    def validate(self, data):
        data = super().validate(data)

        ingredients = data["ingredients"]
        ingredients_ids = [
            ingredient["ingredient"]["id"] for ingredient in ingredients
        ]
        if len(ingredients) != len(set(ingredients_ids)):
            raise serializers.ValidationError(
                {
                    "detail": "В рецепт нельзя добавлять"
                    " одни и те же ингредиенты несколько раз."
                }
            )
        return data

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")

        recipe = Recipe.objects.create(
            **validated_data, author=self.context["request"].user
        )
        recipe.tags.set(tags)

        recipe_ingredients = []
        for ingredient in ingredients:
            recipe_ingredients.append(
                Recipeingredient(
                    recipe=recipe,
                    ingredient_id=ingredient["ingredient"]["id"],
                    amount=ingredient["amount"],
                )
            )
        Recipeingredient.objects.bulk_create(recipe_ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        Recipeingredient.objects.filter(recipe=instance).delete()

        instance.tags.set(tags)

        recipe_ingredients = []
        for ingredient in ingredients:
            recipe_ingredients.append(
                Recipeingredient(
                    recipe=instance,
                    ingredient_id=ingredient["ingredient"]["id"],
                    amount=ingredient["amount"],
                )
            )
        Recipeingredient.objects.bulk_create(recipe_ingredients)

        return instance

    def to_representation(self, instance):
        return RecipeSerializer(
            instance, context={"request": self.context.get("request")}
        ).data


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализуем избранное"""

    class Meta:
        fields = ("id", "name", "image", "cooking_time")
        model = Recipe


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализуем список покупок"""

    class Meta:
        fields = ("id", "name", "image", "cooking_time")
        model = ShoppingCart

    def to_representation(self, instance):
        return {
            "id": instance.recipe.id,
            "name": instance.recipe.name,
            "image": instance.recipe.image.url,
            "cooking_time": instance.recipe.cooking_time,
        }
