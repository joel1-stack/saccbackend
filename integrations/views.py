from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import MpesaTransaction, MpesaConfiguration
from .serializers import STKPushSerializer, MpesaTransactionSerializer
import uuid
import requests
import base64
from datetime import datetime


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_stk_push(request):
    """Initiate M-Pesa STK Push"""
    serializer = STKPushSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        
        # Get M-Pesa configuration
        try:
            config = MpesaConfiguration.objects.get(is_active=True)
        except MpesaConfiguration.DoesNotExist:
            return Response({'error': 'M-Pesa not configured'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate unique IDs
        checkout_request_id = f"ws_CO_{uuid.uuid4().hex[:10]}"
        merchant_request_id = f"ws_MR_{uuid.uuid4().hex[:10]}"
        
        # Create transaction record
        mpesa_transaction = MpesaTransaction.objects.create(
            checkout_request_id=checkout_request_id,
            merchant_request_id=merchant_request_id,
            transaction_type='stk_push',
            phone_number=data['phone_number'],
            amount=data['amount'],
            account_reference=data['account_reference'],
            transaction_desc=data['transaction_desc'],
            status='initiated'
        )
        
        # In a real implementation, you would call M-Pesa API here
        # For now, we'll simulate the response
        
        return Response({
            'message': 'STK Push initiated successfully',
            'checkout_request_id': checkout_request_id,
            'merchant_request_id': merchant_request_id
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def mpesa_callback(request):
    """Handle M-Pesa callback"""
    # This endpoint receives callbacks from M-Pesa
    # In production, you would verify the callback and update transaction status
    
    callback_data = request.data
    checkout_request_id = callback_data.get('CheckoutRequestID')
    
    try:
        transaction = MpesaTransaction.objects.get(checkout_request_id=checkout_request_id)
        
        if callback_data.get('ResultCode') == '0':
            # Success
            transaction.status = 'completed'
            transaction.mpesa_receipt_number = callback_data.get('MpesaReceiptNumber')
            transaction.result_code = '0'
            transaction.result_desc = 'Success'
        else:
            # Failed
            transaction.status = 'failed'
            transaction.result_code = callback_data.get('ResultCode')
            transaction.result_desc = callback_data.get('ResultDesc')
        
        transaction.save()
        
        return Response({'message': 'Callback processed'})
    
    except MpesaTransaction.DoesNotExist:
        return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mpesa_transactions(request):
    """Get M-Pesa transactions"""
    transactions = MpesaTransaction.objects.all()
    serializer = MpesaTransactionSerializer(transactions, many=True)
    return Response(serializer.data)