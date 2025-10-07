from django.db import models
from django.conf import settings


class Member(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='member_profile')
    member_number = models.CharField(max_length=20, unique=True)
    national_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    address = models.TextField()
    occupation = models.CharField(max_length=100)
    employer = models.CharField(max_length=100, blank=True)
    monthly_income = models.DecimalField(max_digits=15, decimal_places=2)
    next_of_kin_name = models.CharField(max_length=100)
    next_of_kin_phone = models.CharField(max_length=15)
    next_of_kin_relationship = models.CharField(max_length=50)
    membership_fee_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    registration_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.member_number} - {self.user.get_full_name()}"

    class Meta:
        ordering = ['-registration_date']


class MemberDocument(models.Model):
    DOCUMENT_TYPES = [
        ('id_copy', 'ID Copy'),
        ('passport_photo', 'Passport Photo'),
        ('payslip', 'Payslip'),
        ('bank_statement', 'Bank Statement'),
        ('other', 'Other'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_file = models.FileField(upload_to='member_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.member_number} - {self.document_type}"