from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ShareAccount, ShareTransaction, DividendPayout
from .serializers import ShareAccountSerializer, ShareTransactionSerializer, SharePurchaseSerializer
from django.db import transaction
import uuid


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def share_account(request):
    """Get user's share account"""
    account, created = ShareAccount.objects.get_or_create(member=request.user)
    serializer = ShareAccountSerializer(account)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def purchase_shares(request):
    """Purchase shares"""
    serializer = SharePurchaseSerializer(data=request.data)
    if serializer.is_valid():
        shares_quantity = serializer.validated_data['shares_quantity']
        
        with transaction.atomic():
            account, created = ShareAccount.objects.get_or_create(member=request.user)
            total_amount = shares_quantity * account.share_price
            
            # Create share transaction
            share_transaction = ShareTransaction.objects.create(
                share_account=account,
                transaction_type='purchase',
                shares_quantity=shares_quantity,
                share_price=account.share_price,
                total_amount=total_amount,
                reference_number=f"SH{uuid.uuid4().hex[:8].upper()}",
                description=f"Purchase of {shares_quantity} shares"
            )
            
            # Update share account
            account.total_shares += shares_quantity
            account.share_balance += total_amount
            account.save()
            
            return Response({
                'message': 'Shares purchased successfully',
                'transaction': ShareTransactionSerializer(share_transaction).data
            })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def share_transactions(request):
    """Get user's share transaction history"""
    account = ShareAccount.objects.filter(member=request.user).first()
    if account:
        transactions = ShareTransaction.objects.filter(share_account=account)
        serializer = ShareTransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    return Response([])