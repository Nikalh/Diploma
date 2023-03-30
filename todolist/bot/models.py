import os

from django.db import models

from todolist.core.models import User
from todolist.goals.models import GoalCategory


class TgUser(models.Model):
    """ Модель с полями:
     chat_id - уникальный номер чата
     user - пользователь (связь с моделью User)
     verification_code - верификационный код
     state - статус пользователя при выполнении команд
     category - категория (связь с моделью GoalCategory)
     """
    chat_id = models.BigIntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    verification_code = models.CharField(max_length=50, null=True, blank=True, default=None)
    state = models.PositiveSmallIntegerField(default=0)
    category = models.ForeignKey(GoalCategory, on_delete=models.DO_NOTHING, null=True, blank=True)

    @staticmethod
    def _generate_verification_code() -> str:
        """ Функция для генерирования кода верификации """
        return os.urandom(12).hex()

    def set_verification_code(self) -> str:
        """ Функция для установки кода верификации и записи в базу данных для TgUser"""
        code = self._generate_verification_code()
        self.verification_code = code
        self.save(update_fields=('verification_code',))
        return code
