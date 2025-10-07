from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'user', 'account_type', 'balance', 'status', 'created_at']
    list_filter = ['account_type', 'status', 'created_at']
    search_fields = ['account_number', 'user__username', 'user__email']
    readonly_fields = ['account_number', 'created_at', 'updated_at']