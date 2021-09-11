#from django.contrib.admin.decorators import display
from django.db import models
from django.contrib.auth import get_user_model
#from django.db.models import constraints
from django.core.validators import MinValueValidator

#from users.models import User #?

User = get_user_model()


class Tag(models.Model):
    title = models.CharField(verbose_name='Название',
                             max_length=50, unique=True)
    slug = models.SlugField(
        verbose_name='Имя тега в шаблоне', max_length=20, unique=True)
    color = models.CharField(verbose_name='Цвет тега', max_length=20)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_recipe", verbose_name='Автор'
    )
    name = models.CharField(max_length=100, verbose_name='Название рецепта')
    image = models.ImageField(
        upload_to="recipes/images/", blank=True, null=True, verbose_name='Картинка')
    text = models.TextField(verbose_name='Текст')
    cooking_time = models.PositiveIntegerField(
        validators= [MinValueValidator(1)])  # verbose_name='Время приготовления'
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Дата публикации')
    tags = models.ManyToManyField(Tag, related_name='tags')
    ingredients = models.ManyToManyField('Ingredient', through='Recipeingredient')

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorites", verbose_name='Пользователь'
    ) #! тут имена с одинаковым названием эт норм?
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="favorites", verbose_name='Рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_user_recipe'
            )
        ]
        verbose_name = 'Объект избранного'
        verbose_name_plural = 'Объекты избранного'

    def __str__(self):
        return f'Избранный {self.recipe} у {self.user}'


class Ingredient(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    dimension = models.CharField(
        max_length=50, verbose_name='Единицы измерения')

    class Meta:
        ordering = ('title', )
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return f'{self.title} ({self.dimension})'


class Recipeingredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="ingredient_recipe")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe')
    amount = models.FloatField(verbose_name='Количество', validators=[
                               MinValueValidator(0), ], )

    class Meta:
        verbose_name = 'Ингридиент в рецепте'
        verbose_name_plural = 'Ингридиенты в рецептах'

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shop_list", verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shop_list')
    amount = models.FloatField(verbose_name='Количество', validators=[
                               MinValueValidator(0), ], )
