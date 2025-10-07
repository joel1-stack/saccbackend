from django.urls import path
from . import views

urlpatterns = [
    path('mpesa/stk-push/', views.initiate_stk_push, name='mpesa-stk-push'),
    path('mpesa/callback/', views.mpesa_callback, name='mpesa-callback'),
    path('mpesa/transactions/', views.mpesa_transactions, name='mpesa-transactions'),
]