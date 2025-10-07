from django.db import models
from django.conf import settings


class ReportSchedule(models.Model):
    REPORT_TYPES = [
        ('financial_statement', 'Financial Statement'),
        ('loan_portfolio', 'Loan Portfolio Report'),
        ('member_summary', 'Member Summary'),
        ('transaction_report', 'Transaction Report'),
        ('share_capital', 'Share Capital Report'),
    ]

    FREQUENCIES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    ]

    name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=30, choices=REPORT_TYPES)
    frequency = models.CharField(max_length=20, choices=FREQUENCIES)
    recipients = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='scheduled_reports')
    is_active = models.BooleanField(default=True)
    last_generated = models.DateTimeField(null=True, blank=True)
    next_generation = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.frequency}"