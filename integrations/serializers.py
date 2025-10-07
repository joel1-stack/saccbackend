from rest_framework import serializers
from .models import MpesaConfiguration, MpesaTransaction, SMSConfiguration


class MpesaConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaConfiguration
        fields = ['id', 'name', 'business_shortcode', 'is_active', 'is_sandbox']
        # Exclude sensitive fields from serialization


class MpesaTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaTransaction
        fields = ['id', 'checkout_request_id', 'phone_number', 'amount', 'account_reference', 
                 'status', 'mpesa_receipt_number', 'created_at']


class STKPushSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    amount = serializers.DecimalField(max_digits=15, decimal_places=2, min_value=1)
    account_reference = serializers.CharField(max_length=50)
    transaction_desc = serializers.CharField(max_length=200)


class SMSConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSConfiguration
        fields = ['id', 'provider', 'sender_id', 'is_active']
        # Exclude API key from serialization