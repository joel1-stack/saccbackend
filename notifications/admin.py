from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'title', 'notification_type', 'is_read', 'is_sent', 'created_at']
    list_filter = ['notification_type', 'is_read', 'is_sent', 'created_at']
    search_fields = ['recipient__username', 'title', 'message']
    readonly_fields = ['created_at', 'sent_at']