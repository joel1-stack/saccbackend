from django.db import models
from django.conf import settings
from loans.models import Loan


class GuarantorLimit(models.Model):
    member = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guarantor_limit')
    max_guarantee_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    current_guarantee_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def available_guarantee_amount(self):
        return self.max_guarantee_amount - self.current_guarantee_amount

    def __str__(self):
        return f"{self.member.username} - Limit: {self.max_guarantee_amount}"


class GuarantorRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('expired', 'Expired'),
    ]

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='guarantor_requests')
    guarantor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guarantee_requests')
    requested_amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    request_message = models.TextField(blank=True)
    response_message = models.TextField(blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['loan', 'guarantor']
        ordering = ['-requested_at']

    def __str__(self):
        return f"{self.guarantor.username} guaranteeing {self.requested_amount} for {self.loan.loan_number}"