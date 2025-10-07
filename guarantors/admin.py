from django.contrib import admin
from .models import GuarantorRequest, GuarantorLimit


@admin.register(GuarantorRequest)
class GuarantorRequestAdmin(admin.ModelAdmin):
    list_display = ['loan', 'guarantor', 'requested_amount', 'status', 'requested_at']
    list_filter = ['status', 'requested_at']
    search_fields = ['loan__loan_number', 'guarantor__username', 'guarantor__first_name', 'guarantor__last_name']
    readonly_fields = ['requested_at', 'responded_at']


@admin.register(GuarantorLimit)
class GuarantorLimitAdmin(admin.ModelAdmin):
    list_display = ['member', 'max_guarantee_amount', 'current_guarantee_amount', 'available_guarantee_amount']
    search_fields = ['member__username', 'member__first_name', 'member__last_name']
    readonly_fields = ['created_at', 'updated_at']

    def available_guarantee_amount(self, obj):
        return obj.available_guarantee_amount()
    available_guarantee_amount.short_description = 'Available Amount'