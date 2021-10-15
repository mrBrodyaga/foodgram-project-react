from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    password = models.CharField('password', max_length=128)
    email = models.EmailField(unique=True, blank=False)
    first_name = models.TextField(max_length=256, blank=False)
    last_name = models.TextField(max_length=256, blank=False)
    subscribers = models.ManyToManyField(
        "User",
        through="Subscription",
        through_fields=("follower", "following"),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        ordering = ["id"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Subscription(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followings",
        verbose_name="Подписчик",
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers",
        verbose_name="На кого подписка",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"], name="subscription_unique"
            ),
        ]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
