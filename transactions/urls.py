from django.urls import path
from . import views

urlpatterns = [
    path('', views.TransactionListView.as_view(), name='transaction-list'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('transfer/', views.transfer, name='transfer'),
]