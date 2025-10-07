from django.db import models
from django.conf import settings
from accounts.models import Account


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
        ('loan_payment', 'Loan Payment'),
        ('interest', 'Interest'),
        ('fee', 'Fee'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    balance_before = models.DecimalField(max_digits=15, decimal_places=2)
    balance_after = models.DecimalField(max_digits=15, decimal_places=2)
    reference_number = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    
    # For transfers
    recipient_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_transfers')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reference_number} - {self.transaction_type}"

    class Meta:
        ordering = ['-created_at']