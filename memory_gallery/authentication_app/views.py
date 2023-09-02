from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from rest_framework.permissions import AllowAny
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from .serializers import CustomUserSerializer, CustomUserRegistrationSerializer, CustomPasswordResetSerializer

# API endpoint for user registration
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = CustomUserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        email_address = EmailAddress.objects.get(user=user, primary=True)
        email_address.verified = True
        email_address.save()
        send_email_confirmation(request, email_address)
        return Response({'message': 'Registration successful. Confirmation email sent.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API endpoint for user login
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        if user.is_active:
            login(request, user)
            return Response({'message': 'Login successful'})
        return Response({'message': 'Account is not active'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API endpoint for user logout
@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logout successful'})

# API endpoint for user profile
@api_view(['GET'])
def user_profile(request):
    serializer = CustomUserSerializer(request.user)
    return Response(serializer.data)

# API endpoint for initiating password reset
@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_view(request):
    serializer = CustomPasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Password reset email sent.'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API endpoint for password reset confirmation
@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm_view(request, uidb64, token):
    serializer = CustomPasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Password reset successful.'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API endpoint for updating user profile
@api_view(['PUT'])
def update_profile(request):
    user = request.user
    serializer = CustomUserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Profile updated successfully'})
                                    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
