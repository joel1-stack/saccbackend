from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Member, MemberDocument
from .serializers import MemberSerializer, MemberRegistrationSerializer, MemberDocumentSerializer


class MemberListView(generics.ListAPIView):
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Member.objects.all()
        return Member.objects.filter(user=self.request.user)


class MemberDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Member.objects.all()
        return Member.objects.filter(user=self.request.user)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def register_member(request):
    if request.method == 'GET':
        return Response({
            'message': 'Complete member registration endpoint - POST your member data here',
            'required_fields': {
                'username': 'string',
                'email': 'string',
                'first_name': 'string',
                'last_name': 'string',
                'phone_number': 'string (unique)',
                'password': 'string',
                'national_id': 'string (unique)',
                'date_of_birth': 'YYYY-MM-DD',
                'address': 'string',
                'occupation': 'string',
                'employer': 'string (optional)',
                'monthly_income': 'decimal',
                'next_of_kin_name': 'string',
                'next_of_kin_phone': 'string',
                'next_of_kin_relationship': 'string'
            },
            'example': {
                'username': 'jane_doe',
                'email': 'jane@example.com',
                'first_name': 'Jane',
                'last_name': 'Doe',
                'phone_number': '+254712345678',
                'password': 'securepass123',
                'national_id': '12345678',
                'date_of_birth': '1990-01-01',
                'address': '123 Main St, Nairobi',
                'occupation': 'Teacher',
                'employer': 'ABC School',
                'monthly_income': '50000.00',
                'next_of_kin_name': 'John Doe',
                'next_of_kin_phone': '+254712345679',
                'next_of_kin_relationship': 'Spouse'
            }
        })
    
    serializer = MemberRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        member = serializer.save()
        return Response(MemberSerializer(member).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def member_profile(request):
    try:
        member = Member.objects.get(user=request.user)
        return Response(MemberSerializer(member).data)
    except Member.DoesNotExist:
        return Response({'error': 'Member profile not found'}, status=status.HTTP_404_NOT_FOUND)


class MemberDocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = MemberDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            member = Member.objects.get(user=self.request.user)
            return MemberDocument.objects.filter(member=member)
        except Member.DoesNotExist:
            return MemberDocument.objects.none()

    def perform_create(self, serializer):
        member = Member.objects.get(user=self.request.user)
        serializer.save(member=member)