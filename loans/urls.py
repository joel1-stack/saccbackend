from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoanListView.as_view(), name='loan-list'),
    path('<int:pk>/', views.LoanDetailView.as_view(), name='loan-detail'),
    path('apply/', views.apply_loan, name='apply-loan'),
    path('<int:loan_id>/approve/', views.approve_loan, name='approve-loan'),
    path('<int:loan_id>/payment/', views.make_payment, name='make-payment'),
]