from rest_framework import serializers
from .models import ReportSchedule


class ReportScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportSchedule
        fields = ['id', 'name', 'report_type', 'frequency', 'is_active', 'last_generated', 'next_generation']


class DashboardStatsSerializer(serializers.Serializer):
    total_members = serializers.IntegerField()
    total_accounts = serializers.IntegerField()
    total_savings = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_loans = serializers.IntegerField()
    total_loan_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    active_loans = serializers.IntegerField()
    pending_loans = serializers.IntegerField()


class FinancialStatementSerializer(serializers.Serializer):
    period = serializers.CharField()
    total_deposits = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_withdrawals = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_loan_disbursements = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_loan_repayments = serializers.DecimalField(max_digits=15, decimal_places=2)
    net_cash_flow = serializers.DecimalField(max_digits=15, decimal_places=2)