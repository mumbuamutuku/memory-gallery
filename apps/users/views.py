from django.contrib.auth import get_user_model, authenticate, login
from rest_framework import generics, permissions, status
from rest_framework.decorators import permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import render
from rest_framework.request import Request
from .models import CustomUserManager, CustomUser, UserProfile
from .serializers import CustomUserSerializer, UserProfileSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404


User = get_user_model()

class WelcomeAPIView(APIView):
    def get(self, request):
        context = {
            'message': 'Welcome to the Memory Gallery!',
        }
        return render(request, 'index.html', context)

class RegistrationAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([AllowAny])
class UserLoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            user_data = {
               'token': token.key,
               'user_id': user.id,
               'username': user.username
            }

            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileAPIView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = ()
    authentication_classes = ()
    lookup_field = 'pk'

    def get_object(self):
        user_id = self.kwargs.get(self.lookup_field)
        user_profile = UserProfile.objects.filter(pk=user_id).select_related('user').first()

        if not user_profile:
            raise NotFound("User profile not found")

        return user_profile

    def get(self, request, *args, **kwargs):
        user_profile = self.get_object()
        serializer = self.serializer_class(user_profile)

        # Include username and email in the response
        response_data = serializer.data
        response_data['username'] = user_profile.username
        response_data['email'] = user_profile.email

        return Response(response_data)
