from django.db import models
from todolist.core.models import User


class BaseModel(models.Model):
    """ Создаем Базовую модель, в которой указываются поля:
        created - Дата создания
        updated - Дата последнего обновления
    """
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата последнего обновления', auto_now=True)

    class Meta:
        abstract = True


class Board(BaseModel):
    """ Создаем модель Доски, в которой указываются поля:
        title - название категории
        is_deleted - статус категории (по умолчанию = не удалена)
    """

    class Meta:
        verbose_name = 'Доска'
        verbose_name_plural = 'Доски'

    title = models.CharField(verbose_name='Название', max_length=255)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)


class BoardParticipant(BaseModel):
    """ Создаем модель Участник доски, в которой присутствуют поля:
        board - связь с моделью Board
        user - связь с моделью User
        role - роль участника (по умолчанию = владелец)
    """

    class Meta:
        unique_together = ('board', 'user')
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    class Role(models.IntegerChoices):
        owner = 1, 'Владелец'
        writer = 2, 'Редактор'
        reader = 3, 'Читатель'

    board = models.ForeignKey(
        Board,
        verbose_name='Доска',
        on_delete=models.PROTECT,
        related_name='participants',
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.PROTECT,
        related_name='participants',
    )
    role = models.PositiveSmallIntegerField(verbose_name='Роль', choices=Role.choices, default=Role.owner)


class GoalCategory(BaseModel):
    """ Создаем модель Категорий, в которой указываются поля:
        title - название категории
        board - связь с моделью Board
        user - связь с моделью User
        is_deleted - статус категории (по умолчанию = не удалена)
    """
    board = models.ForeignKey(Board, verbose_name='Доска', on_delete=models.PROTECT, related_name='categories')
    title = models.CharField(verbose_name='Название', max_length=255)
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title


class Goal(BaseModel):
    """ Создаем модель Цели, в которой указывается статус (по умолчанию = к выполнению),
        приоритет (по умолчанию = средний). Также присутствуют поля:
        title - название цели
        description - описание цели (может быть не заполнено)
        category - связь с моделью GoalCategory
        due_date - дата завершения
        user - связь с моделью User
    """

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
    """ Создаем модель Комментарий к цели, в которой указывается:
        goal - связь с моделью Goal
        user - связь с моделью User
        text - текст комментария
    """
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.PROTECT)
    text = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return self.text
