from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    ]
    
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    is_verified = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - {self.role}"