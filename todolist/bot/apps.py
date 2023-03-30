from django.apps import AppConfig

""" Конфигурация для бота в проекте"""


class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todolist.bot'
