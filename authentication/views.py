from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'GET':
        return Response({
            'message': 'Login endpoint - POST your credentials here',
            'required_fields': {
                'username': 'string',
                'password': 'string'
            },
            'example': {
                'username': 'your_username',
                'password': 'your_password'
            }
        })
    
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'GET':
        return Response({
            'message': 'User registration endpoint - POST your registration data here',
            'required_fields': {
                'username': 'string',
                'email': 'string',
                'first_name': 'string',
                'last_name': 'string',
                'phone_number': 'string (unique)',
                'password': 'string (min 6 chars)',
                'password_confirm': 'string (must match password)'
            },
            'example': {
                'username': 'john_doe',
                'email': 'john@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'phone_number': '+254712345678',
                'password': 'securepass123',
                'password_confirm': 'securepass123'
            }
        })
    
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)