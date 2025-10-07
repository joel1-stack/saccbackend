from django.urls import path
from . import views

urlpatterns = [
    path('account/', views.share_account, name='share-account'),
    path('purchase/', views.purchase_shares, name='purchase-shares'),
    path('transactions/', views.share_transactions, name='share-transactions'),
]