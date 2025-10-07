// Frontend Configuration for Angular App
// Add this to your Angular environment files

export const environment = {
  production: true,
  apiUrl: 'https://saccbackend.vercel.app/api',
  frontendUrl: 'https://sacco-sigma.vercel.app'
};

// For development
export const environmentDev = {
  production: false,
  apiUrl: 'http://localhost:8000/api',
  frontendUrl: 'http://localhost:4200'
};

// Update your Angular services to use these URLs:
// Example: this.http.post(`${environment.apiUrl}/auth/login/`, loginData)