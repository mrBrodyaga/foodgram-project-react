from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name="Название", max_length=50, unique=True
    )
    slug = models.SlugField(
        verbose_name="Имя тега в шаблоне", max_length=20, unique=True
    )
    color = models.CharField(verbose_name="Цвет тега", max_length=20)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="author_recipe",
        verbose_name="Автор",
    )
    name = models.CharField(max_length=100, verbose_name="Название рецепта")
    image = models.ImageField(
        upload_to="recipes/images/",
        blank=True,
        null=True,
        verbose_name="Картинка",
    )
    text = models.TextField(verbose_name="Текст")
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Дата публикации"
    )
    tags = models.ManyToManyField(Tag, related_name="tags")
    ingredients = models.ManyToManyField(
        "Ingredient", through="Recipeingredient"
    )
    favorited_by = models.ManyToManyField(
        User, through="Favorite", related_name="favorite_recipes"
    )
    is_in_shopping_cart = models.ManyToManyField(
        User, through="ShoppingCart", related_name="recipes_in_shopping_cart"
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Рецепт",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_favorite_user_recipe"
            )
        ]
        verbose_name = "Объект избранного"
        verbose_name_plural = "Объекты избранного"

    def __str__(self):
        return f"Избранный {self.recipe} у {self.user}"


class Ingredient(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    measurement_unit = models.CharField(
        max_length=50, verbose_name="Единицы измерения"
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f"{self.name} ({self.measurement_unit})"


class Recipeingredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="ingredient_recipe"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipe"
    )
    amount = models.FloatField(
        verbose_name="Количество",
        validators=[
            MinValueValidator(1),
        ],
    )

    class Meta:
        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецептах"

    def __str__(self):
        return f"{self.ingredient} в {self.recipe}"


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shop_list",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="shop_list"
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"

    def __str__(self):
        return f"{self.user} в {self.recipe}"
