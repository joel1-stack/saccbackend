from django.urls import path
from . import views

urlpatterns = [
    path('', views.notifications_list, name='notifications-list'),
    path('<int:notification_id>/read/', views.mark_as_read, name='mark-notification-read'),
    path('broadcast/', views.broadcast_notification, name='broadcast-notification'),
]