from django.contrib import admin

from todolist.goals.models import GoalCategory, GoalComment, Goal


class GoalCategoryAdmin(admin.ModelAdmin):
    """Указываем поля, которые будут отображаться в панели администратора для категорий"""
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'user')


class GoalAdmin(admin.ModelAdmin):
    """Указываем поля, которые будут отображаться в панели администратора для целей"""
    list_display = ('user', 'category', 'description', 'status', 'priority', 'due_date', 'created', 'updated')
    search_fields = ('title', 'user')


class GoalCommentAdmin(admin.ModelAdmin):
    """Указываем поля, которые будут отображаться в панели администратора для комментариев"""
    list_display = ('goal', 'user', 'text', 'created', 'updated')
    search_fields = ('title', 'user')

# Регистрируем админку
admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)
