from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Account
        fields = ['id', 'account_number', 'account_type', 'balance', 'status', 'interest_rate', 'user_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'account_number', 'balance', 'created_at', 'updated_at']