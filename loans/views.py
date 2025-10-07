from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Loan, LoanPayment
from .serializers import LoanSerializer, LoanApplicationSerializer, LoanPaymentSerializer


class LoanListView(generics.ListAPIView):
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Loan.objects.all()
        return Loan.objects.filter(user=self.request.user)


class LoanDetailView(generics.RetrieveAPIView):
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Loan.objects.all()
        return Loan.objects.filter(user=self.request.user)


@api_view(['GET', 'POST'])
def apply_loan(request):
    if request.method == 'GET':
        return Response({
            'message': 'Loan application endpoint - POST your loan application here',
            'required_fields': {
                'loan_type': 'personal|business|emergency|asset',
                'amount_requested': 'decimal',
                'interest_rate': 'decimal',
                'term_months': 'integer',
                'purpose': 'string',
                'collateral': 'string (optional)'
            },
            'example': {
                'loan_type': 'personal',
                'amount_requested': '50000.00',
                'interest_rate': '12.00',
                'term_months': 24,
                'purpose': 'Business expansion',
                'collateral': 'Property deed'
            }
        })
    
    serializer = LoanApplicationSerializer(data=request.data)
    if serializer.is_valid():
        # Generate loan number
        import random
        loan_number = f"LN{random.randint(100000, 999999)}"
        loan = serializer.save(user=request.user, loan_number=loan_number)
        return Response(LoanSerializer(loan).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def approve_loan(request, loan_id):
    if request.user.role != 'admin':
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        loan = Loan.objects.get(id=loan_id)
        loan.status = 'approved'
        loan.amount_approved = request.data.get('amount_approved', loan.amount_requested)
        # Calculate monthly payment
        principal = float(loan.amount_approved)
        rate = float(loan.interest_rate) / 100 / 12
        months = loan.term_months
        if rate > 0:
            loan.monthly_payment = principal * (rate * (1 + rate)**months) / ((1 + rate)**months - 1)
        else:
            loan.monthly_payment = principal / months
        loan.balance_remaining = loan.amount_approved
        loan.save()
        return Response(LoanSerializer(loan).data)
    except Loan.DoesNotExist:
        return Response({'error': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def make_payment(request, loan_id):
    try:
        loan = Loan.objects.get(id=loan_id, user=request.user)
        serializer = LoanPaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save(loan=loan)
            # Update loan balance
            loan.balance_remaining -= payment.amount
            if loan.balance_remaining <= 0:
                loan.status = 'completed'
                loan.balance_remaining = 0
            loan.save()
            return Response(LoanPaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Loan.DoesNotExist:
        return Response({'error': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)