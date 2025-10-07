from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_stats, name='dashboard-stats'),
    path('financial-statement/', views.financial_statement, name='financial-statement'),
    path('loan-portfolio/', views.loan_portfolio_report, name='loan-portfolio'),
]