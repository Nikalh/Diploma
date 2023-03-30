from rest_framework import permissions

from todolist.goals.models import BoardParticipant, Board, GoalCategory, Goal, GoalComment


class BoardPermissions(permissions.IsAuthenticated):
    """ Создаем разрешение для доски, в котором проверяется роль пользователя"""
    def has_object_permission(self, request, view, obj: Board):
        _filters: dict = {'user_id': request.user.id, 'board_id': obj.id}
        if request.method not in permissions.SAFE_METHODS:
            _filters['role'] = BoardParticipant.Role.owner
        return BoardParticipant.objects.filter(**_filters).exists()


class GoalCategoryPermissions(permissions.IsAuthenticated):
    """ Создаем разрешение для категории, в котором проверяется роль пользователя"""
    def has_object_permission(self, request, view, obj: GoalCategory):
        _filters: dict = {'user_id': request.user.id, 'board_id': obj.board_id}
        if request.method not in permissions.SAFE_METHODS:
            _filters['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        return BoardParticipant.objects.filter(**_filters).exists()


class GoalPermissions(permissions.IsAuthenticated):
    """ Создаем разрешение для цели, в котором проверяется роль пользователя"""
    def has_object_permission(self, request, view, obj: Goal):
        _filters: dict = {'user_id': request.user.id, 'board_id': obj.category.board_id}
        if request.method not in permissions.SAFE_METHODS:
            _filters['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        return BoardParticipant.objects.filter(**_filters).exists()


class GoalCommentPermissions(permissions.IsAuthenticated):
    """ Создаем разрешение для комментария цели, в котором проверяется пользователь"""
    def has_object_permission(self, request, view, obj: GoalComment):
        return request.method in permissions.SAFE_METHODS or obj.user_id == request.user.id
