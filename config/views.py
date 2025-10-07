from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import Account
from loans.models import Loan
from transactions.models import Transaction
from members.models import Member


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    user = request.user
    
    if user.role == 'admin':
        # Admin dashboard
        data = {
            'total_members': Member.objects.count(),
            'total_accounts': Account.objects.count(),
            'total_loans': Loan.objects.count(),
            'pending_loans': Loan.objects.filter(status='pending').count(),
            'total_transactions': Transaction.objects.count(),
            'total_deposits': sum(t.amount for t in Transaction.objects.filter(transaction_type='deposit')),
            'total_withdrawals': sum(t.amount for t in Transaction.objects.filter(transaction_type='withdrawal')),
        }
    else:
        # Member dashboard
        try:
            member = Member.objects.get(user=user)
            accounts = Account.objects.filter(user=user)
            loans = Loan.objects.filter(user=user)
            transactions = Transaction.objects.filter(user=user)[:10]  # Recent 10 transactions
            
            data = {
                'member_info': {
                    'member_number': member.member_number,
                    'name': user.get_full_name(),
                    'status': member.status,
                },
                'accounts_summary': {
                    'total_accounts': accounts.count(),
                    'total_balance': sum(acc.balance for acc in accounts),
                    'accounts': [{'id': acc.id, 'account_number': acc.account_number, 'type': acc.account_type, 'balance': acc.balance} for acc in accounts]
                },
                'loans_summary': {
                    'total_loans': loans.count(),
                    'active_loans': loans.filter(status='active').count(),
                    'total_balance': sum(loan.balance_remaining for loan in loans.filter(status='active')),
                },
                'recent_transactions': [
                    {
                        'id': t.id,
                        'type': t.transaction_type,
                        'amount': t.amount,
                        'description': t.description,
                        'date': t.created_at,
                        'reference': t.reference_number
                    } for t in transactions
                ]
            }
        except Member.DoesNotExist:
            data = {'error': 'Member profile not found'}
    
    return Response(data)