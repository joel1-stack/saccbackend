from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Account
from .serializers import AccountSerializer


class AccountListCreateView(generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Account.objects.all()
        return Account.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        # Handle both list and create form display
        accounts = self.get_queryset()
        serializer = self.get_serializer(accounts, many=True)
        
        return Response({
            'accounts': serializer.data,
            'create_account_info': {
                'message': 'To create a new account, POST to this endpoint',
                'required_fields': {
                    'account_type': 'savings|current|fixed_deposit',
                    'interest_rate': 'decimal (optional)'
                },
                'example': {
                    'account_type': 'savings',
                    'interest_rate': '2.50'
                }
            }
        })

    def perform_create(self, serializer):
        # Generate account number
        import random
        account_number = f"ACC{random.randint(100000, 999999)}"
        serializer.save(user=self.request.user, account_number=account_number)


class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Account.objects.all()
        return Account.objects.filter(user=self.request.user)


@api_view(['GET'])
def account_summary(request):
    accounts = Account.objects.filter(user=request.user)
    total_balance = sum(account.balance for account in accounts)
    return Response({
        'total_accounts': accounts.count(),
        'total_balance': total_balance,
        'accounts': AccountSerializer(accounts, many=True).data
    })