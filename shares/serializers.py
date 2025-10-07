from rest_framework import serializers
from .models import ShareAccount, ShareTransaction, DividendPayout
from authentication.serializers import UserSerializer


class ShareAccountSerializer(serializers.ModelSerializer):
    member = UserSerializer(read_only=True)
    total_value = serializers.SerializerMethodField()

    class Meta:
        model = ShareAccount
        fields = ['id', 'member', 'total_shares', 'share_balance', 'share_price', 'total_value', 'created_at']

    def get_total_value(self, obj):
        return obj.total_shares * obj.share_price


class ShareTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareTransaction
        fields = ['id', 'transaction_type', 'shares_quantity', 'share_price', 'total_amount', 
                 'reference_number', 'description', 'created_at']


class SharePurchaseSerializer(serializers.Serializer):
    shares_quantity = serializers.IntegerField(min_value=1)
    payment_method = serializers.ChoiceField(choices=[('savings', 'From Savings'), ('mpesa', 'M-Pesa')])


class DividendPayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = DividendPayout
        fields = ['id', 'year', 'dividend_rate', 'total_dividend_pool', 'payout_date', 'is_processed']