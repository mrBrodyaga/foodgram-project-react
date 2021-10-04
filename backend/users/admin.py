from django.contrib import admin

from .models import Subscription, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Регестируем модель пользователя"""

    list_display = ("username", "email", "first_name", "last_name")
    list_filter = (
        "username",
        "email",
    )
    empty_value_display = "-пусто-"


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Регестируем модель подписок"""

    list_display = ("follower", "following")
    list_filter = ("follower", "following")
    empty_value_display = "-пусто-"
