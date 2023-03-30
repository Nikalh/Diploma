
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

""" Конфигурация URL проекта.
    Список `urlpatterns` URLs для вью проекта.
"""
urlpatterns = [
    path('core/', include(('todolist.core.urls', 'todolist.core'))),
    path('bot/', include(('todolist.bot.urls', 'todolist.bot'))),
    path('goals/', include(('todolist.goals.urls', 'todolist.goals'))),
    path('admin/', admin.site.urls),
    path('oauth/', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    urlpatterns += [
        path('api-auth/', include('rest_framework.urls')),

    ]
