# Frontend Integration Guide

## Field Mapping Reference

To avoid frontend-backend field mismatches, use these exact field names:

### Authentication
**Login**: `username`, `password`
**Register**: `username`, `email`, `first_name`, `last_name`, `phone_number`, `password`

### Member Registration
```typescript
{
  username: string,
  email: string,
  first_name: string,
  last_name: string,
  phone_number: string,  // NOT 'phone'
  password: string,
  national_id: string,
  date_of_birth: string, // YYYY-MM-DD format
  address: string,
  occupation: string,
  employer?: string,
  monthly_income: number,
  next_of_kin_name: string,
  next_of_kin_phone: string,
  next_of_kin_relationship: string
}
```

### Account Creation
```typescript
{
  account_type: 'savings' | 'current' | 'fixed_deposit',
  interest_rate?: number
}
```

### Loan Application
```typescript
{
  loan_type: 'personal' | 'business' | 'emergency' | 'asset',
  amount_requested: number,
  interest_rate: number,
  term_months: number,
  purpose: string,
  collateral?: string
}
```

### Transactions
**Deposit/Withdrawal**:
```typescript
{
  account_id: number,
  amount: number,
  description: string
}
```

**Transfer**:
```typescript
{
  from_account_id: number,
  to_account_number: string,
  amount: number,
  description: string
}
```

## API Endpoints Summary

### Core Endpoints
- `GET/POST /api/auth/login/` - User authentication
- `GET/POST /api/auth/register/` - User registration
- `GET /api/dashboard/` - Dashboard data (requires auth)
- `GET/POST /api/accounts/` - Account management
- `GET /api/accounts/summary/` - Account summary
- `GET /api/loans/` - User loans
- `GET/POST /api/loans/apply/` - Loan application
- `GET /api/transactions/` - Transaction history
- `GET/POST /api/transactions/deposit/` - Make deposit
- `GET/POST /api/transactions/withdraw/` - Make withdrawal
- `GET/POST /api/transactions/transfer/` - Transfer funds
- `GET /api/members/` - Member list (admin) or profile
- `GET/POST /api/members/register/` - Member registration
- `GET /api/members/profile/` - Member profile

### Authentication Headers
```typescript
headers: {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
}
```

## Common Pitfalls to Avoid

1. **Field Names**: Use exact backend field names (snake_case, not camelCase)
2. **Date Format**: Use YYYY-MM-DD for dates
3. **Phone Numbers**: Use `phone_number` not `phone`
4. **Names**: Use `first_name`/`last_name` not `firstName`/`lastName`
5. **Authentication**: Always include Bearer token for protected endpoints
6. **Error Handling**: Backend returns field-specific errors in `errors` object

## Testing Your Integration

1. Run the test script: `python test_api_endpoints.py`
2. Check all endpoints return 200 OK for documentation
3. Test actual operations with proper authentication
4. Verify field mappings match exactly