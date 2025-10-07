from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import GuarantorRequest, GuarantorLimit
from .serializers import GuarantorRequestSerializer, GuarantorLimitSerializer
from django.utils import timezone


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def guarantor_requests_received(request):
    """List all guarantor requests sent to current user"""
    requests = GuarantorRequest.objects.filter(guarantor=request.user)
    serializer = GuarantorRequestSerializer(requests, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respond_to_guarantor_request(request, request_id):
    """Approve or decline a guarantor request"""
    try:
        guarantor_request = GuarantorRequest.objects.get(id=request_id, guarantor=request.user)
        action = request.data.get('action')  # 'approved' or 'declined'
        response_message = request.data.get('response_message', '')

        if action not in ['approved', 'declined']:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

        guarantor_request.status = action
        guarantor_request.response_message = response_message
        guarantor_request.responded_at = timezone.now()
        guarantor_request.save()

        # Update guarantor limit if approved
        if action == 'approved':
            limit, created = GuarantorLimit.objects.get_or_create(member=request.user)
            limit.current_guarantee_amount += guarantor_request.requested_amount
            limit.save()

        return Response({'message': f'Request {action} successfully'})
    except GuarantorRequest.DoesNotExist:
        return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def guarantor_limit(request):
    """Get current user's guarantor limit"""
    try:
        limit = GuarantorLimit.objects.get(member=request.user)
        serializer = GuarantorLimitSerializer(limit)
        return Response(serializer.data)
    except GuarantorLimit.DoesNotExist:
        return Response({'max_guarantee_amount': 0, 'current_guarantee_amount': 0, 'available_amount': 0})