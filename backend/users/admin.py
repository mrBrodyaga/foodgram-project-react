from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """ Регестируем модель пользователя"""

    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email',)
    empty_value_display = '-пусто-'
