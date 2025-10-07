# SACCO Nova Backend

A comprehensive Django REST API backend for the SACCO Nova financial management system.

## Features

- **User Authentication & Authorization** - JWT-based authentication with role-based access
- **Account Management** - Multiple account types (Savings, Current, Fixed Deposit)
- **Loan Management** - Loan applications, approvals, and payment tracking
- **Transaction Processing** - Deposits, withdrawals, and transfers
- **Member Management** - Member registration and profile management
- **Admin Dashboard** - Administrative oversight and reporting

## Technology Stack

- **Framework**: Django 4.2.7
- **API**: Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (Simple JWT)
- **Real-time**: Django Channels + Redis
- **File Storage**: Django File Storage

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL
- Redis (for WebSocket support)

### Installation

1. **Clone and navigate to the project**
   ```bash
   cd sacco-nova-backend
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```

3. **Configure environment variables**
   Update the `.env` file with your database credentials:
   ```env
   DATABASE_NAME=saccodata
   DATABASE_USER=postgres
   DATABASE_PASSWORD=your-password
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   ```

4. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `GET /api/auth/profile/` - Get user profile
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Dashboard
- `GET /api/dashboard/` - Get dashboard summary

### Accounts
- `GET /api/accounts/` - List user accounts
- `POST /api/accounts/` - Create new account
- `GET /api/accounts/{id}/` - Get account details
- `GET /api/accounts/summary/` - Get accounts summary

### Loans
- `GET /api/loans/` - List user loans
- `POST /api/loans/apply/` - Apply for a loan
- `GET /api/loans/{id}/` - Get loan details
- `POST /api/loans/{id}/approve/` - Approve loan (admin only)
- `POST /api/loans/{id}/payment/` - Make loan payment

### Transactions
- `GET /api/transactions/` - List user transactions
- `POST /api/transactions/deposit/` - Make a deposit
- `POST /api/transactions/withdraw/` - Make a withdrawal
- `POST /api/transactions/transfer/` - Transfer funds

### Members
- `GET /api/members/` - List members (admin) or get own profile
- `POST /api/members/register/` - Register new member
- `GET /api/members/profile/` - Get member profile
- `POST /api/members/documents/` - Upload member documents

## Database Models

### User (Custom User Model)
- Extended Django User with phone number, role, and verification status

### Member
- Member profile with personal and financial information
- Links to User model

### Account
- Bank accounts with different types and balances
- Links to User model

### Loan
- Loan applications and management
- Payment tracking and status management

### Transaction
- All financial transactions (deposits, withdrawals, transfers)
- Complete audit trail

## Security Features

- JWT-based authentication
- Role-based access control (Member, Admin, Staff)
- CORS configuration for frontend integration
- Input validation and sanitization
- Secure file upload handling

## Development

### Project Structure
```
sacco-nova-backend/
├── authentication/     # User authentication and management
├── accounts/          # Account management
├── loans/             # Loan processing
├── transactions/      # Transaction handling
├── members/           # Member management
├── config/            # Django configuration
├── requirements.txt   # Python dependencies
├── .env              # Environment variables
└── manage.py         # Django management script
```

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Deployment

For production deployment:

1. Set `DEBUG=False` in environment variables
2. Configure proper database settings
3. Set up Redis for WebSocket support
4. Configure static file serving
5. Set up proper logging
6. Use a production WSGI server (e.g., Gunicorn)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.