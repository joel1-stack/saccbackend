# Frontend API Integration Guide

## Base Configuration

```typescript
// environment.ts
export const environment = {
  production: false,
  apiUrl: 'http://127.0.0.1:8000/api'
};
```

## API Service Examples

### 1. Authentication Service

```typescript
// auth.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  login(credentials: {username: string, password: string}): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/login/`, credentials);
  }

  register(userData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/register/`, userData);
  }

  getProfile(): Observable<any> {
    return this.http.get(`${this.apiUrl}/auth/profile/`);
  }

  refreshToken(refreshToken: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/token/refresh/`, {
      refresh: refreshToken
    });
  }
}
```

### 2. Dashboard Service

```typescript
// dashboard.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getDashboardSummary(): Observable<any> {
    return this.http.get(`${this.apiUrl}/dashboard/`);
  }
}
```

### 3. Account Service

```typescript
// account.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AccountService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getAccounts(): Observable<any> {
    return this.http.get(`${this.apiUrl}/accounts/`);
  }

  createAccount(accountData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/accounts/`, accountData);
  }

  getAccountSummary(): Observable<any> {
    return this.http.get(`${this.apiUrl}/accounts/summary/`);
  }

  getAccount(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/accounts/${id}/`);
  }
}
```

### 4. Transaction Service

```typescript
// transaction.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class TransactionService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getTransactions(): Observable<any> {
    return this.http.get(`${this.apiUrl}/transactions/`);
  }

  deposit(depositData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/transactions/deposit/`, depositData);
  }

  withdraw(withdrawData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/transactions/withdraw/`, withdrawData);
  }

  transfer(transferData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/transactions/transfer/`, transferData);
  }
}
```

### 5. Loan Service

```typescript
// loan.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class LoanService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getLoans(): Observable<any> {
    return this.http.get(`${this.apiUrl}/loans/`);
  }

  applyForLoan(loanData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/loans/apply/`, loanData);
  }

  getLoan(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/loans/${id}/`);
  }

  makePayment(loanId: number, paymentData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/loans/${loanId}/payment/`, paymentData);
  }

  approveLoan(loanId: number, approvalData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/loans/${loanId}/approve/`, approvalData);
  }
}
```

### 6. Member Service

```typescript
// member.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class MemberService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  registerMember(memberData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/members/register/`, memberData);
  }

  getMembers(): Observable<any> {
    return this.http.get(`${this.apiUrl}/members/`);
  }

  getMemberProfile(): Observable<any> {
    return this.http.get(`${this.apiUrl}/members/profile/`);
  }

  uploadDocument(documentData: FormData): Observable<any> {
    return this.http.post(`${this.apiUrl}/members/documents/`, documentData);
  }

  getDocuments(): Observable<any> {
    return this.http.get(`${this.apiUrl}/members/documents/`);
  }
}
```

## HTTP Interceptor for Authentication

```typescript
// auth.interceptor.ts
import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler } from '@angular/common/http';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler) {
    const token = localStorage.getItem('access_token');
    
    if (token) {
      const authReq = req.clone({
        headers: req.headers.set('Authorization', `Bearer ${token}`)
      });
      return next.handle(authReq);
    }
    
    return next.handle(req);
  }
}
```

## Sample API Calls

### Login Example
```typescript
// login.component.ts
login() {
  const credentials = {
    username: this.loginForm.value.username,
    password: this.loginForm.value.password
  };

  this.authService.login(credentials).subscribe({
    next: (response) => {
      localStorage.setItem('access_token', response.access);
      localStorage.setItem('refresh_token', response.refresh);
      localStorage.setItem('user', JSON.stringify(response.user));
      // Navigate to dashboard
    },
    error: (error) => {
      console.error('Login failed:', error);
    }
  });
}
```

### Dashboard Data Example
```typescript
// dashboard.component.ts
ngOnInit() {
  this.dashboardService.getDashboardSummary().subscribe({
    next: (data) => {
      this.dashboardData = data;
    },
    error: (error) => {
      console.error('Failed to load dashboard:', error);
    }
  });
}
```

### Create Account Example
```typescript
// account.component.ts
createAccount() {
  const accountData = {
    account_type: 'savings',
    interest_rate: '2.50'
  };

  this.accountService.createAccount(accountData).subscribe({
    next: (response) => {
      console.log('Account created:', response);
      this.loadAccounts(); // Refresh account list
    },
    error: (error) => {
      console.error('Failed to create account:', error);
    }
  });
}
```

## Error Handling

```typescript
// error.service.ts
import { Injectable } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ErrorService {
  handleError(error: HttpErrorResponse) {
    if (error.status === 401) {
      // Redirect to login
      localStorage.clear();
      // Navigate to login page
    } else if (error.status === 400) {
      // Handle validation errors
      return error.error;
    } else if (error.status === 500) {
      // Handle server errors
      console.error('Server error:', error);
    }
    return error;
  }
}
```

All endpoints are now ready for your Angular frontend integration!