from django.contrib import admin
from .models import Loan, LoanPayment


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['loan_number', 'user', 'loan_type', 'amount_requested', 'amount_approved', 'status', 'application_date']
    list_filter = ['loan_type', 'status', 'application_date']
    search_fields = ['loan_number', 'user__username', 'user__email']
    readonly_fields = ['loan_number', 'application_date', 'created_at', 'updated_at']


@admin.register(LoanPayment)
class LoanPaymentAdmin(admin.ModelAdmin):
    list_display = ['loan', 'amount', 'payment_date', 'reference_number']
    list_filter = ['payment_date']
    search_fields = ['loan__loan_number', 'reference_number']