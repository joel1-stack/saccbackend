from django.db import models
from django.conf import settings


class Loan(models.Model):
    LOAN_TYPES = [
        ('personal', 'Personal Loan'),
        ('business', 'Business Loan'),
        ('emergency', 'Emergency Loan'),
        ('asset', 'Asset Financing'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('defaulted', 'Defaulted'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loans')
    loan_number = models.CharField(max_length=20, unique=True)
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    amount_requested = models.DecimalField(max_digits=15, decimal_places=2)
    amount_approved = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_months = models.IntegerField()
    monthly_payment = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    balance_remaining = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    purpose = models.TextField()
    collateral = models.TextField(blank=True)
    application_date = models.DateTimeField(auto_now_add=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    disbursement_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.loan_number} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']


class LoanPayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    reference_number = models.CharField(max_length=50)
    
    def __str__(self):
        return f"Payment {self.amount} for {self.loan.loan_number}"