from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Создаем модель Пользователя унаследовав от модели AbstractUser"""
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
