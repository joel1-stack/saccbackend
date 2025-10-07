# SACCO Nova API Documentation

## Base URL
```
http://localhost:8000/api/
```

## Authentication

All endpoints except registration and login require JWT authentication.

### Headers
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

## API Endpoints

### 1. Authentication

#### Login
```http
POST /auth/login/
```

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "refresh": "string",
  "access": "string",
  "user": {
    "id": 1,
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "phone_number": "string",
    "role": "member|admin|staff"
  }
}
```

#### Register
```http
POST /auth/register/
```

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "phone_number": "string",
  "password": "string",
  "password_confirm": "string"
}
```

### 2. Dashboard

#### Get Dashboard Summary
```http
GET /dashboard/
```

**Response (Member):**
```json
{
  "member_info": {
    "member_number": "string",
    "name": "string",
    "status": "active"
  },
  "accounts_summary": {
    "total_accounts": 2,
    "total_balance": "5000.00",
    "accounts": [...]
  },
  "loans_summary": {
    "total_loans": 1,
    "active_loans": 1,
    "total_balance": "10000.00"
  },
  "recent_transactions": [...]
}
```

### 3. Accounts

#### List Accounts
```http
GET /accounts/
```

#### Create Account
```http
POST /accounts/
```

**Request Body:**
```json
{
  "account_type": "savings|current|fixed_deposit",
  "interest_rate": "2.50"
}
```

#### Get Account Summary
```http
GET /accounts/summary/
```

### 4. Loans

#### List Loans
```http
GET /loans/
```

#### Apply for Loan
```http
POST /loans/apply/
```

**Request Body:**
```json
{
  "loan_type": "personal|business|emergency|asset",
  "amount_requested": "50000.00",
  "interest_rate": "12.00",
  "term_months": 24,
  "purpose": "Business expansion",
  "collateral": "Property deed"
}
```

#### Approve Loan (Admin Only)
```http
POST /loans/{loan_id}/approve/
```

**Request Body:**
```json
{
  "amount_approved": "45000.00"
}
```

#### Make Loan Payment
```http
POST /loans/{loan_id}/payment/
```

**Request Body:**
```json
{
  "amount": "2000.00",
  "reference_number": "PAY123456"
}
```

### 5. Transactions

#### List Transactions
```http
GET /transactions/
```

#### Make Deposit
```http
POST /transactions/deposit/
```

**Request Body:**
```json
{
  "account_id": 1,
  "amount": "1000.00",
  "description": "Salary deposit"
}
```

#### Make Withdrawal
```http
POST /transactions/withdraw/
```

**Request Body:**
```json
{
  "account_id": 1,
  "amount": "500.00",
  "description": "ATM withdrawal"
}
```

#### Transfer Funds
```http
POST /transactions/transfer/
```

**Request Body:**
```json
{
  "from_account_id": 1,
  "to_account_number": "ACC123456",
  "amount": "1000.00",
  "description": "Transfer to friend"
}
```

### 6. Members

#### Register Member
```http
POST /members/register/
```

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "phone_number": "string",
  "password": "string",
  "national_id": "string",
  "date_of_birth": "1990-01-01",
  "address": "string",
  "occupation": "string",
  "employer": "string",
  "monthly_income": "50000.00",
  "next_of_kin_name": "string",
  "next_of_kin_phone": "string",
  "next_of_kin_relationship": "string"
}
```

#### Get Member Profile
```http
GET /members/profile/
```

#### Upload Documents
```http
POST /members/documents/
```

**Request Body (multipart/form-data):**
```
document_type: id_copy|passport_photo|payslip|bank_statement|other
document_file: <file>
```

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "error": "Permission denied"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

## Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error