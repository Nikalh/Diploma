from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters

from todolist.goals.filters import GoalDateFilter
from todolist.goals.models import GoalCategory, Goal, GoalComment, BoardParticipant, Board
from todolist.goals.permissions import BoardPermissions, GoalCategoryPermissions, GoalPermissions, \
    GoalCommentPermissions
from todolist.goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, \
    GoalSerializer, GoalCommentSerializer, GoalCommentCreateSerializer, BoardCreateSerializer, BoardSerializer


class BoardCreateView(CreateAPIView):
    """ Создаем вью создания доски"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer

    def perform_create(self, serializer):
        # переопределяем метод
        BoardParticipant.objects.create(user=self.request.user, board=serializer.save())


class BoardListView(ListAPIView):
    """ Создаем вью получения списка досок"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['title']

    def get_queryset(self):
        # получаем данные отфильтровав по пользователю и тому что доска не удалена
        return Board.objects.filter(participants__user_id=self.request.user.id, is_deleted=False)


class BoardView(RetrieveUpdateDestroyAPIView):
    """ Создаем вью получения, обновления и удаления доски"""
    permission_classes = [BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        # получаем данные отфильтровав по тому что доска не удалена
        return Board.objects.filter(is_deleted=False)

    def perform_destroy(self, instance: Board):
        # переопределяем метод удаления для помещения в архив
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)


class GoalCategoryCreateView(CreateAPIView):
    """ Создаем вью создания категории"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    """ Создаем вью получения списка категорий с возможностью фильтрации"""
    permission_classes = [GoalCategoryPermissions]
    serializer_class = GoalCategorySerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, ]
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title']

    def get_queryset(self):
        # получаем данные отфильтровав по пользователю и тому что категория не удалена
        return GoalCategory.objects.filter(
            board__participants__user_id=self.request.user.id, is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    """ Создаем вью получения, обновления и удаления категории"""
    serializer_class = GoalCategorySerializer
    permission_classes = [GoalCategoryPermissions]

    def get_queryset(self):
        # получаем данные отфильтровав по пользователю и тому что категория не удалена
        return GoalCategory.objects.filter(
            board__participants__user_id=self.request.user.id, is_deleted=False)

    def perform_destroy(self, instance: GoalCategory):
        # переопределяем метод удаления для помещения в архив
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.goals.update(status=Goal.Status.archived)


class GoalCreateView(CreateAPIView):
    """ Создаем вью создания цели"""
    serializer_class = GoalCreateSerializer
    permission_classes = [GoalPermissions]


class GoalListView(ListAPIView):
    """ Создаем вью получения списка целей с возможностью фильтрации"""
    serializer_class = GoalSerializer
    permission_classes = [GoalPermissions]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title', 'description']

    def get_queryset(self):
        # получаем данные отфильтровав по пользователю и тому что категория не удалена исключив цели в архиве
        return Goal.objects.filter(
            category__board__participants__user_id=self.request.user.id, category__is_deleted=False
        ).exclude(status=Goal.Status.archived)


class GoalView(RetrieveUpdateDestroyAPIView):
    """ Создаем вью получения, обновления и удаления цели"""
    serializer_class = GoalSerializer
    permission_classes = [GoalPermissions]

    def get_queryset(self):
        # получаем данные отфильтровав по пользователю и тому что категория не удалена исключив цели в архиве
        return Goal.objects.filter(
            category__board__participants__user_id=self.request.user.id,
            category__is_deleted=False,
        ).exclude(status=Goal.Status.archived)

    def perform_destroy(self, instance: Goal):
        # переопределяем метод удаления
        instance.status = Goal.Status.archived
        instance.save(update_fields=('status',))


class GoalCommentCreateView(CreateAPIView):
    """ Создаем вью создания комментария к цели"""
    permission_classes = [GoalCommentPermissions]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(ListAPIView):
    """ Создаем вью на получение списка комментариев к цели с возможностью фильтрации"""
    permission_classes = [GoalCommentPermissions]
    serializer_class = GoalCommentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['goal']
    ordering_fields = ['-created']
    ordering = ['created']

    def get_queryset(self):
        # получаем данные отфильтровав по пользователю
        return GoalComment.objects.filter(goal__category__board__participants__user_id=self.request.user.id, )


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    """ Создаем вью получения, обновления и удаления комментария к цели"""
    serializer_class = GoalCommentSerializer
    permission_classes = [GoalCommentPermissions]

    def get_queryset(self):
        # получаем данные отфильтровав по пользователю
        return GoalComment.objects.select_related('user').filter(user_id=self.request.user.id)
