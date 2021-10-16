from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from api.models import Recipe

from .models import Subscription, User


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name"]


class CustomUserSerializer(UserSerializer):
    """Сериализуем Пользователя для получения информации о нём"""

    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        user = request.user

        if user.is_anonymous:
            return False

        is_subscribed = Subscription.objects.filter(
            follower=user, following=obj
        ).exists()  # noqa: R504

        return is_subscribed  # noqa: R504

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
        fields = "__all__"


class SubscribeToSerializer(serializers.ModelSerializer):
    """Сериализуем подписки"""

    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        requester = self.context.get("requester")
        if not requester:
            return False
        return Subscription.objects.filter(
            follower=requester, following=obj
        ).exists()

    def get_recipes_count(self, obj):
        author_id = obj.id
        count = Recipe.objects.filter(
            author_id=author_id).count()  # noqa: R504
        return count  # noqa: R504

    def get_recipes(self, obj):
        author_id = obj.id
        qs = Recipe.objects.filter(author_id=author_id)
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
            "recipes",
            "recipes_count",
        )


class CustomSetPasswordSerializer(serializers.Serializer):
    """Сериализуем информацию для изменения пароля"""

    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)
