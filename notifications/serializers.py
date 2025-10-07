from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'notification_type', 'is_read', 'created_at']


class NotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['recipient', 'title', 'message', 'notification_type', 'channels']


class BroadcastNotificationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    message = serializers.CharField()
    notification_type = serializers.ChoiceField(choices=Notification.NOTIFICATION_TYPES)
    channels = serializers.ListField(child=serializers.CharField())
    recipient_type = serializers.ChoiceField(choices=[('all', 'All Members'), ('staff', 'Staff Only')])