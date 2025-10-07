from django.db import models
from django.conf import settings


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('loan_approval', 'Loan Approval'),
        ('loan_rejection', 'Loan Rejection'),
        ('payment_due', 'Payment Due'),
        ('payment_received', 'Payment Received'),
        ('guarantor_request', 'Guarantor Request'),
        ('share_purchase', 'Share Purchase'),
        ('dividend_payout', 'Dividend Payout'),
        ('system_announcement', 'System Announcement'),
        ('account_activity', 'Account Activity'),
    ]

    CHANNELS = [
        ('in_app', 'In-App'),
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
    ]

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    channels = models.JSONField(default=list)  # ['in_app', 'sms', 'email']
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipient.username} - {self.title}"