from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer, BroadcastNotificationSerializer
from authentication.models import User
from django.utils import timezone


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notifications_list(request):
    """Get user's notifications"""
    notifications = Notification.objects.filter(recipient=request.user)
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_as_read(request, notification_id):
    """Mark notification as read"""
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user)
        notification.is_read = True
        notification.save()
        return Response({'message': 'Notification marked as read'})
    except Notification.DoesNotExist:
        return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def broadcast_notification(request):
    """Broadcast notification to all members (admin only)"""
    if request.user.role != 'admin':
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = BroadcastNotificationSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        recipient_type = data['recipient_type']
        
        if recipient_type == 'all':
            recipients = User.objects.all()
        else:
            recipients = User.objects.filter(role__in=['admin', 'staff'])
        
        notifications = []
        for recipient in recipients:
            notifications.append(Notification(
                recipient=recipient,
                title=data['title'],
                message=data['message'],
                notification_type=data['notification_type'],
                channels=data['channels']
            ))
        
        Notification.objects.bulk_create(notifications)
        return Response({'message': f'Notification sent to {len(notifications)} recipients'})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def create_notification(recipient, title, message, notification_type, channels=['in_app']):
    """Helper function to create notifications"""
    return Notification.objects.create(
        recipient=recipient,
        title=title,
        message=message,
        notification_type=notification_type,
        channels=channels
    )