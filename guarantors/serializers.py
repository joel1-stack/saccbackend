from rest_framework import serializers
from .models import GuarantorRequest, GuarantorLimit
from authentication.serializers import UserSerializer


class GuarantorLimitSerializer(serializers.ModelSerializer):
    member = UserSerializer(read_only=True)
    available_amount = serializers.SerializerMethodField()

    class Meta:
        model = GuarantorLimit
        fields = ['id', 'member', 'max_guarantee_amount', 'current_guarantee_amount', 'available_amount']

    def get_available_amount(self, obj):
        return obj.available_guarantee_amount()


class GuarantorRequestSerializer(serializers.ModelSerializer):
    guarantor = UserSerializer(read_only=True)
    loan_details = serializers.SerializerMethodField()

    class Meta:
        model = GuarantorRequest
        fields = ['id', 'loan', 'guarantor', 'requested_amount', 'status', 'request_message', 
                 'response_message', 'requested_at', 'responded_at', 'loan_details']

    def get_loan_details(self, obj):
        return {
            'loan_number': obj.loan.loan_number,
            'applicant': obj.loan.user.get_full_name(),
            'amount': obj.loan.amount_requested
        }


class GuarantorRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuarantorRequest
        fields = ['loan', 'guarantor', 'requested_amount', 'request_message']