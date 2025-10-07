from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from .models import Transaction
from .serializers import TransactionSerializer, DepositSerializer, WithdrawalSerializer, TransferSerializer
from accounts.models import Account
import uuid


class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Transaction.objects.all()
        return Transaction.objects.filter(user=self.request.user)


@api_view(['GET', 'POST'])
def deposit(request):
    if request.method == 'GET':
        return Response({
            'message': 'Deposit endpoint - POST your deposit data here',
            'required_fields': {
                'account_id': 'integer',
                'amount': 'decimal',
                'description': 'string'
            },
            'example': {
                'account_id': 1,
                'amount': '1000.00',
                'description': 'Salary deposit'
            }
        })
    
    serializer = DepositSerializer(data=request.data)
    if serializer.is_valid():
        try:
            account = Account.objects.get(id=serializer.validated_data['account_id'], user=request.user)
            amount = serializer.validated_data['amount']
            
            with transaction.atomic():
                balance_before = account.balance
                account.balance += amount
                account.save()
                
                trans = Transaction.objects.create(
                    user=request.user,
                    account=account,
                    transaction_type='deposit',
                    amount=amount,
                    balance_before=balance_before,
                    balance_after=account.balance,
                    reference_number=f"DEP{uuid.uuid4().hex[:8].upper()}",
                    description=serializer.validated_data['description'],
                    status='completed'
                )
                
            return Response(TransactionSerializer(trans).data, status=status.HTTP_201_CREATED)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def withdraw(request):
    if request.method == 'GET':
        return Response({
            'message': 'Withdrawal endpoint - POST your withdrawal data here',
            'required_fields': {
                'account_id': 'integer',
                'amount': 'decimal',
                'description': 'string'
            },
            'example': {
                'account_id': 1,
                'amount': '500.00',
                'description': 'ATM withdrawal'
            }
        })
    
    serializer = WithdrawalSerializer(data=request.data)
    if serializer.is_valid():
        try:
            account = Account.objects.get(id=serializer.validated_data['account_id'], user=request.user)
            amount = serializer.validated_data['amount']
            
            if account.balance < amount:
                return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
            
            with transaction.atomic():
                balance_before = account.balance
                account.balance -= amount
                account.save()
                
                trans = Transaction.objects.create(
                    user=request.user,
                    account=account,
                    transaction_type='withdrawal',
                    amount=amount,
                    balance_before=balance_before,
                    balance_after=account.balance,
                    reference_number=f"WTH{uuid.uuid4().hex[:8].upper()}",
                    description=serializer.validated_data['description'],
                    status='completed'
                )
                
            return Response(TransactionSerializer(trans).data, status=status.HTTP_201_CREATED)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def transfer(request):
    if request.method == 'GET':
        return Response({
            'message': 'Transfer endpoint - POST your transfer data here',
            'required_fields': {
                'from_account_id': 'integer',
                'to_account_number': 'string',
                'amount': 'decimal',
                'description': 'string'
            },
            'example': {
                'from_account_id': 1,
                'to_account_number': 'ACC123456',
                'amount': '1000.00',
                'description': 'Transfer to friend'
            }
        })
    
    serializer = TransferSerializer(data=request.data)
    if serializer.is_valid():
        try:
            from_account = Account.objects.get(id=serializer.validated_data['from_account_id'], user=request.user)
            to_account = Account.objects.get(account_number=serializer.validated_data['to_account_number'])
            amount = serializer.validated_data['amount']
            
            if from_account.balance < amount:
                return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
            
            with transaction.atomic():
                # Debit from sender
                from_balance_before = from_account.balance
                from_account.balance -= amount
                from_account.save()
                
                # Credit to recipient
                to_balance_before = to_account.balance
                to_account.balance += amount
                to_account.save()
                
                ref_number = f"TRF{uuid.uuid4().hex[:8].upper()}"
                
                # Create debit transaction
                debit_trans = Transaction.objects.create(
                    user=request.user,
                    account=from_account,
                    transaction_type='transfer',
                    amount=amount,
                    balance_before=from_balance_before,
                    balance_after=from_account.balance,
                    reference_number=ref_number,
                    description=f"Transfer to {to_account.account_number}: {serializer.validated_data['description']}",
                    recipient_account=to_account,
                    status='completed'
                )
                
                # Create credit transaction
                Transaction.objects.create(
                    user=to_account.user,
                    account=to_account,
                    transaction_type='transfer',
                    amount=amount,
                    balance_before=to_balance_before,
                    balance_after=to_account.balance,
                    reference_number=ref_number,
                    description=f"Transfer from {from_account.account_number}: {serializer.validated_data['description']}",
                    status='completed'
                )
                
            return Response(TransactionSerializer(debit_trans).data, status=status.HTTP_201_CREATED)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)