#!/usr/bin/env python3
"""
SACCO Nova Backend Setup Script
This script helps set up the Django backend for the SACCO Nova application.
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    print("🚀 Setting up SACCO Nova Backend...")
    
    # Check if virtual environment exists
    if not os.path.exists('venv'):
        print("\n📦 Creating virtual environment...")
        if not run_command('python -m venv venv', 'Virtual environment creation'):
            return False
    
    # Activate virtual environment and install dependencies
    if os.name == 'nt':  # Windows
        activate_cmd = 'venv\\Scripts\\activate && '
    else:  # Unix/Linux/macOS
        activate_cmd = 'source venv/bin/activate && '
    
    commands = [
        (f'{activate_cmd}pip install -r requirements.txt', 'Installing dependencies'),
        (f'{activate_cmd}python manage.py makemigrations', 'Creating migrations'),
        (f'{activate_cmd}python manage.py migrate', 'Running migrations'),
        (f'{activate_cmd}python manage.py collectstatic --noinput', 'Collecting static files'),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    print("\n✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update the .env file with your database credentials")
    print("2. Create a superuser: python manage.py createsuperuser")
    print("3. Start the development server: python manage.py runserver")
    print("\n🔗 API Endpoints will be available at:")
    print("- Authentication: http://localhost:8000/api/auth/")
    print("- Accounts: http://localhost:8000/api/accounts/")
    print("- Loans: http://localhost:8000/api/loans/")
    print("- Transactions: http://localhost:8000/api/transactions/")
    print("- Members: http://localhost:8000/api/members/")
    print("- Dashboard: http://localhost:8000/api/dashboard/")

if __name__ == '__main__':
    main()