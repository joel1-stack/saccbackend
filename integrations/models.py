from django.db import models
from django.conf import settings


class MpesaConfiguration(models.Model):
    name = models.CharField(max_length=100, default='Default')
    consumer_key = models.CharField(max_length=200)
    consumer_secret = models.CharField(max_length=200)
    business_shortcode = models.CharField(max_length=20)
    passkey = models.CharField(max_length=200)
    callback_url = models.URLField()
    is_active = models.BooleanField(default=True)
    is_sandbox = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'M-Pesa Configuration'
        verbose_name_plural = 'M-Pesa Configurations'

    def __str__(self):
        return f"{self.name} - {self.business_shortcode}"


class MpesaTransaction(models.Model):
    STATUS_CHOICES = [
        ('initiated', 'Initiated'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    TRANSACTION_TYPES = [
        ('stk_push', 'STK Push'),
        ('b2c', 'Business to Customer'),
        ('c2b', 'Customer to Business'),
        ('reversal', 'Reversal'),
    ]

    checkout_request_id = models.CharField(max_length=100, unique=True)
    merchant_request_id = models.CharField(max_length=100)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    account_reference = models.CharField(max_length=50)
    transaction_desc = models.CharField(max_length=200)
    mpesa_receipt_number = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='initiated')
    result_code = models.CharField(max_length=10, blank=True, null=True)
    result_desc = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.checkout_request_id} - {self.amount}"


class SMSConfiguration(models.Model):
    provider = models.CharField(max_length=50)  # 'africastalking', 'twilio', etc.
    api_key = models.CharField(max_length=200)
    username = models.CharField(max_length=100, blank=True)
    sender_id = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.provider} - {self.sender_id}"