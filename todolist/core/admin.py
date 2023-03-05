from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_filter = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('email', 'first_name', 'last_name')}),
        ('Разрешения', {'fields': ('is_active', 'is_superuser', 'is_staff')}),
        ('Особенные даты', {'fields': ('last_login', 'date_joined')}),

    )

#admin.site.register(User)
