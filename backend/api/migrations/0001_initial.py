# Generated by Django 3.1 on 2021-08-03 12:51

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Объект избранного',
                'verbose_name_plural': 'Объекты избранного',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('dimension', models.CharField(max_length=50, verbose_name='Единицы измерения')),
            ],
            options={
                'verbose_name': 'Ингридиент',
                'verbose_name_plural': 'Ингридиенты',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название рецепта')),
                ('image', models.ImageField(blank=True, null=True, upload_to='recipes/images/', verbose_name='Картинка')),
                ('text', models.TextField(verbose_name='Текст')),
                ('cooking_time', models.PositiveIntegerField(verbose_name=django.core.validators.MinValueValidator(1))),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Recipeingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'Ингридиент в рецепте',
                'verbose_name_plural': 'Ингридиенты в рецептах',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('Завтрак', 'Breakfast'), ('Обед', 'Lunch'), ('Ужин', 'Dinner')], max_length=50, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(max_length=20, unique=True, verbose_name='Имя тега в шаблоне')),
                ('color', models.CharField(max_length=20, verbose_name='Цвет тега')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_list', to='api.recipe')),
            ],
        ),
    ]