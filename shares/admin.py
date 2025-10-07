from django.contrib import admin
from .models import ShareAccount, ShareTransaction, DividendPayout


@admin.register(ShareAccount)
class ShareAccountAdmin(admin.ModelAdmin):
    list_display = ['member', 'total_shares', 'share_balance', 'share_price', 'created_at']
    search_fields = ['member__username', 'member__first_name', 'member__last_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ShareTransaction)
class ShareTransactionAdmin(admin.ModelAdmin):
    list_display = ['reference_number', 'share_account', 'transaction_type', 'shares_quantity', 'total_amount', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['reference_number', 'share_account__member__username']
    readonly_fields = ['created_at']


@admin.register(DividendPayout)
class DividendPayoutAdmin(admin.ModelAdmin):
    list_display = ['year', 'dividend_rate', 'total_dividend_pool', 'payout_date', 'is_processed']
    list_filter = ['is_processed', 'year']
    readonly_fields = ['created_at']