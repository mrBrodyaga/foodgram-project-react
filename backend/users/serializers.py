from api.serializers import RecipeSerializer
from api.models import Recipe
from rest_framework import serializers
from djoser.serializers import UserSerializer

from .models import Subscription, User


class CustomUserSerializer(UserSerializer):
    """Сериализуем Пользователя для получеяния информации о нём"""
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        if not user:
            return False
        return Subscription.objects.filter(follower=user, following=obj).exists()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )


class RecipeSubscriptionSerializer(serializers.ModelSerializer):
    """Сериализуем рецепты подписки"""

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализуем подписки"""

    class Meta:
        model = Subscription
        fields = '__all__'


class SubscribeToSerializer(serializers.ModelSerializer):
    """Сериализуем подписки"""
    recipes_count = serializers.SerializerMethodField()
    recipe = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = None
        request = self.context.get("request")
        dir(request)
        if request and hasattr(request, "user"):
            user = request.user
            print(user)
            print(request)
        if not user:
            print(user)
            print(request)
            return False
        return Subscription.objects.filter(follower=user, following=obj).exists()

    def get_recipes_count(self, obj):
        author_id = obj.id
        count = Recipe.objects.filter(id=author_id).count()
        return count

    def get_recipe(self, obj):
        author_id = obj.id
        qs = Recipe.objects.filter(id=author_id)
        return RecipeSubscriptionSerializer(qs, many=True).data

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            'recipe',
            'recipes_count',
        )
