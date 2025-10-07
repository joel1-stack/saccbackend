from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_verified', 'is_active']
    list_filter = ['role', 'is_verified', 'is_active', 'date_joined']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'role', 'is_verified', 'two_factor_enabled')}),
    )