from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count
from members.models import Member
from accounts.models import Account
from loans.models import Loan
from transactions.models import Transaction
from shares.models import ShareAccount
from .serializers import DashboardStatsSerializer, FinancialStatementSerializer
from datetime import datetime, timedelta


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Get dashboard statistics"""
    if request.user.role not in ['admin', 'staff']:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    stats = {
        'total_members': Member.objects.count(),
        'total_accounts': Account.objects.count(),
        'total_savings': Account.objects.aggregate(total=Sum('balance'))['total'] or 0,
        'total_loans': Loan.objects.count(),
        'total_loan_amount': Loan.objects.aggregate(total=Sum('amount_requested'))['total'] or 0,
        'active_loans': Loan.objects.filter(status='active').count(),
        'pending_loans': Loan.objects.filter(status='pending').count(),
    }
    
    serializer = DashboardStatsSerializer(stats)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def financial_statement(request):
    """Get financial statement for a period"""
    if request.user.role not in ['admin', 'staff']:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    # Get date range from query params
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if not start_date or not end_date:
        # Default to current month
        today = datetime.now()
        start_date = today.replace(day=1)
        end_date = today
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    transactions = Transaction.objects.filter(
        created_at__range=[start_date, end_date],
        status='completed'
    )
    
    deposits = transactions.filter(transaction_type='deposit').aggregate(total=Sum('amount'))['total'] or 0
    withdrawals = transactions.filter(transaction_type='withdrawal').aggregate(total=Sum('amount'))['total'] or 0
    loan_disbursements = transactions.filter(transaction_type='loan_disbursement').aggregate(total=Sum('amount'))['total'] or 0
    loan_repayments = transactions.filter(transaction_type='loan_payment').aggregate(total=Sum('amount'))['total'] or 0
    
    statement = {
        'period': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
        'total_deposits': deposits,
        'total_withdrawals': withdrawals,
        'total_loan_disbursements': loan_disbursements,
        'total_loan_repayments': loan_repayments,
        'net_cash_flow': deposits + loan_repayments - withdrawals - loan_disbursements
    }
    
    serializer = FinancialStatementSerializer(statement)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def loan_portfolio_report(request):
    """Get loan portfolio breakdown"""
    if request.user.role not in ['admin', 'staff']:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    portfolio = {
        'total_loans': Loan.objects.count(),
        'active_loans': Loan.objects.filter(status='active').count(),
        'pending_loans': Loan.objects.filter(status='pending').count(),
        'completed_loans': Loan.objects.filter(status='completed').count(),
        'defaulted_loans': Loan.objects.filter(status='defaulted').count(),
        'total_disbursed': Loan.objects.filter(status__in=['active', 'completed']).aggregate(total=Sum('amount_approved'))['total'] or 0,
        'total_outstanding': Loan.objects.filter(status='active').aggregate(total=Sum('balance_remaining'))['total'] or 0,
    }
    
    return Response(portfolio)