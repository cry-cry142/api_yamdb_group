from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Roles(models.TextChoices):
        USER = 'user', 'user'
        MODERATOR = 'moderator', 'moderator'
        ADMIN = 'admin', 'admin'

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True
    )
    role = models.CharField(
        verbose_name='Права доступа',
        max_length=16,
        choices=Roles.choices,
        default=Roles.USER
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    is_moderator = models.BooleanField(
        verbose_name='Пользователь является модератором',
        default=False
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.is_moderator = (self.role == self.Roles.MODERATOR)
        self.is_staff = (self.role == self.Roles.ADMIN) or self.is_superuser
        super().save(*args, **kwargs)
