from django.apps import AppConfig

""" Конфигурация для Core в проекте"""


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todolist.core'
    verbose_name = 'Ядро'
