from rest_framework import serializers
from .models import Loan, LoanPayment


class LoanSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Loan
        fields = ['id', 'loan_number', 'loan_type', 'amount_requested', 'amount_approved', 
                 'interest_rate', 'term_months', 'monthly_payment', 'balance_remaining', 
                 'status', 'purpose', 'collateral', 'user_name', 'application_date', 
                 'approval_date', 'disbursement_date']
        read_only_fields = ['id', 'loan_number', 'amount_approved', 'monthly_payment', 
                           'balance_remaining', 'status', 'approval_date', 'disbursement_date']


class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['loan_type', 'amount_requested', 'interest_rate', 'term_months', 'purpose', 'collateral']


class LoanPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanPayment
        fields = ['id', 'loan', 'amount', 'payment_date', 'reference_number']
        read_only_fields = ['id', 'payment_date']