#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from authentication.models import User

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@sacconova.com',
        password='admin123',
        phone_number='+254700000000',
        role='admin'
    )
    print("Superuser 'admin' created successfully!")
    print("Username: admin")
    print("Password: admin123")
else:
    print("Superuser 'admin' already exists!")