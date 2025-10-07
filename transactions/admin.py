from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['reference_number', 'user', 'account', 'transaction_type', 'amount', 'status', 'created_at']
    list_filter = ['transaction_type', 'status', 'created_at']
    search_fields = ['reference_number', 'user__username', 'account__account_number']
    readonly_fields = ['reference_number', 'balance_before', 'balance_after', 'created_at', 'updated_at']