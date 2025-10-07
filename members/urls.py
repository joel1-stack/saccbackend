from django.urls import path
from . import views

urlpatterns = [
    path('', views.MemberListView.as_view(), name='member-list'),
    path('<int:pk>/', views.MemberDetailView.as_view(), name='member-detail'),
    path('register/', views.register_member, name='register-member'),
    path('profile/', views.member_profile, name='member-profile'),
    path('documents/', views.MemberDocumentListCreateView.as_view(), name='member-documents'),
]