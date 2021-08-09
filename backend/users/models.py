from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=50, blank=False, unique=True)
    password = models.CharField(max_length=100, blank=False)
    email = models.EmailField(unique=True, blank=False)
    first_name = models.TextField(max_length=256, blank=True)
    last_name = models.TextField(max_length=256, blank=True)
    subscribers = models.ManyToManyField(
        'User', through='Subscription', through_fields=('follower', 'following'), )

    class Meta:
        ordering = ["id"]


class Subscription(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followings", verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers", verbose_name='На кого подписка'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'],
                                    name='subscription_unique'),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
