from django.db import models
from django.utils import timezone

from todolist.core.models import User


class BaseModel(models.Model):
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата последнего обновления', auto_now=True)

    # def save(self, *args, **kwargs):
    #     if not self.id:  # Когда объект только создается, у него еще нет id
    #         self.created = timezone.now()  # проставляем дату создания
    #     self.updated = timezone.now()  # проставляем дату обновления
    #     return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class GoalCategory(BaseModel):
    title = models.CharField(verbose_name='Название', max_length=255)
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title


class Goal(BaseModel):
    class Status(models.IntegerChoices):
        to_do = 1, 'К выполнению'
        in_progress = 2, 'В процессе'
        done = 3, 'Выполнено'
        archived = 4, 'Архив'

    class Priority(models.IntegerChoices):
        low = 1, 'Низкий'
        medium = 2, 'Средний'
        high = 3, 'Высокий'
        critical = 4, 'Критический'

    title = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(to=GoalCategory, on_delete=models.PROTECT, related_name='goals')
    due_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name='goals')
    status = models.PositiveSmallIntegerField(verbose_name='Статус', choices=Status.choices, default=Status.to_do)
    priority = models.PositiveSmallIntegerField(verbose_name='Приоритет', choices=Priority.choices,
                                                default=Priority.medium)


    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    def __str__(self) -> str:
        return self.title


class GoalComment(BaseModel):
    #title = models.CharField(verbose_name='Комментарий', max_length=255)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.PROTECT)
    text = models.TextField(null=True, blank=True)

    # is_deleted = models.BooleanField(verbose_name='Удален', default=False)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return self.text
