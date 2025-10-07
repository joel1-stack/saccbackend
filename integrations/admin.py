from django.contrib import admin
from .models import MpesaConfiguration, MpesaTransaction, SMSConfiguration


@admin.register(MpesaConfiguration)
class MpesaConfigurationAdmin(admin.ModelAdmin):
    list_display = ['name', 'business_shortcode', 'is_active', 'is_sandbox', 'created_at']
    list_filter = ['is_active', 'is_sandbox']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MpesaTransaction)
class MpesaTransactionAdmin(admin.ModelAdmin):
    list_display = ['checkout_request_id', 'phone_number', 'amount', 'status', 'mpesa_receipt_number', 'created_at']
    list_filter = ['status', 'transaction_type', 'created_at']
    search_fields = ['checkout_request_id', 'phone_number', 'mpesa_receipt_number']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SMSConfiguration)
class SMSConfigurationAdmin(admin.ModelAdmin):
    list_display = ['provider', 'sender_id', 'is_active', 'created_at']
    list_filter = ['provider', 'is_active']
    readonly_fields = ['created_at']