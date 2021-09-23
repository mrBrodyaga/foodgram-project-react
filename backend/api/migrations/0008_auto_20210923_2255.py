# Generated by Django 3.1 on 2021-09-23 15:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0007_remove_shoppingcart_amount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ('name',), 'verbose_name': 'Ингридиент', 'verbose_name_plural': 'Ингридиенты'},
        ),
        migrations.RenameField(
            model_name='ingredient',
            old_name='dimension',
            new_name='measurement_unit',
        ),
        migrations.RenameField(
            model_name='ingredient',
            old_name='title',
            new_name='name',
        ),
        migrations.AddField(
            model_name='recipe',
            name='favorited_by',
            field=models.ManyToManyField(related_name='favorite_recipes', through='api.Favorite', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recipe',
            name='is_in_shopping_cart',
            field=models.ManyToManyField(related_name='recipes_in_shopping_cart', through='api.ShoppingCart', to=settings.AUTH_USER_MODEL),
        ),
    ]
