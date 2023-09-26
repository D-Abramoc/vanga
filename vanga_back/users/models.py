from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Логин',
        max_length=200,
        unique=True
    )
    password = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username
