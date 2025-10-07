from django.urls import path
from . import views

urlpatterns = [
    path('requests/', views.guarantor_requests_received, name='guarantor-requests'),
    path('requests/<int:request_id>/respond/', views.respond_to_guarantor_request, name='respond-guarantor-request'),
    path('limit/', views.guarantor_limit, name='guarantor-limit'),
]