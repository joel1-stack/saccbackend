from rest_framework import serializers
from .models import Transaction
from accounts.models import Account


class TransactionSerializer(serializers.ModelSerializer):
    account_number = serializers.CharField(source='account.account_number', read_only=True)
    recipient_account_number = serializers.CharField(source='recipient_account.account_number', read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'transaction_type', 'amount', 'balance_before', 'balance_after', 
                 'reference_number', 'description', 'status', 'account_number', 
                 'recipient_account_number', 'created_at']
        read_only_fields = ['id', 'balance_before', 'balance_after', 'reference_number', 'status', 'created_at']


class DepositSerializer(serializers.Serializer):
    account_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    description = serializers.CharField(max_length=255)


class WithdrawalSerializer(serializers.Serializer):
    account_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    description = serializers.CharField(max_length=255)


class TransferSerializer(serializers.Serializer):
    from_account_id = serializers.IntegerField()
    to_account_number = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    description = serializers.CharField(max_length=255)