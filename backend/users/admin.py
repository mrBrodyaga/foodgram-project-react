from django.contrib import admin
#from django.contrib.auth import get_user_model
#from django.contrib.auth.admin import UserAdmin

#from .forms import CustomUserCreationForm, CustomUserChangeForm
#from .models import CustomUser

#class CustomUserAdmin(UserAdmin):
#    add_form = CustomUserCreationForm
#    form = CustomUserChangeForm
#    model = CustomUser
#    list_display = ['username', 'email', 'first_name', 'last_name']
#    list_filter = ('username', 'email')
#    empty_value_display = '-пусто-'

#admin.site.register(CustomUser, CustomUserAdmin)

from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """ Регестируем модель пользователя"""

    list_display = ("username", "email")
