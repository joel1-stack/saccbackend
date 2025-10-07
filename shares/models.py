from django.db import models
from django.conf import settings


class ShareAccount(models.Model):
    member = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='share_account')
    total_shares = models.IntegerField(default=0)
    share_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    share_price = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.member.username} - {self.total_shares} shares"


class ShareTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('purchase', 'Share Purchase'),
        ('sale', 'Share Sale'),
        ('dividend', 'Dividend Payment'),
        ('transfer', 'Share Transfer'),
    ]

    share_account = models.ForeignKey(ShareAccount, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    shares_quantity = models.IntegerField()
    share_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    reference_number = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reference_number} - {self.transaction_type}"


class DividendPayout(models.Model):
    year = models.IntegerField()
    dividend_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Percentage
    total_dividend_pool = models.DecimalField(max_digits=15, decimal_places=2)
    payout_date = models.DateField()
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['year']
        ordering = ['-year']

    def __str__(self):
        return f"Dividend {self.year} - {self.dividend_rate}%"