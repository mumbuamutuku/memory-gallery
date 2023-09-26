from django.contrib.auth import get_user_model, authenticate, login
from rest_framework import generics, permissions, status
from rest_framework.decorators import permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from django.shortcuts import redirect
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import render
from rest_framework.request import Request
from .models import CustomUserManager, CustomUser, UserProfile
from .serializers import CustomUserSerializer, UserProfileSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse


User = get_user_model()

class WelcomeAPIView(APIView):
    def get(self, request):
        context = {
            'message': 'Welcome to the Memory Gallery!',
        }
        return render(request, 'index.html', context)

class RegistrationAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.save()
            
            # Create the user profile with the user's primary key (pk)
            profile_data = {
                'user': user.pk,  # Use the primary key of the user
                'profile_picture': None,
                'bio': '',  # You can set this to the desired initial value
            }
            profile_serializer = UserProfileSerializer(data=profile_data)
            if profile_serializer.is_valid():
                profile_serializer.save()
            else:
                # Handle errors in profile creation, if any
                user.delete()  # Delete the user if profile creation fails
                return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

            #return Response(user_data, status=status.HTTP_200_OK)
            return redirect(reverse('edit-profile'))
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileAPIView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = ()
    authentication_classes = ()
    #permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'

    def get_object(self):
        user_id = self.kwargs.get(self.lookup_field)
        user_profile = UserProfile.objects.filter(pk=user_id).select_related('user').first()
        #user_profile = UserProfile.objects.filter(pk=user_id, user=self.request.user).first()
        
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

class CreateProfileAPIView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def perform_create(self, serializer):
        # Automatically set the user field to the currently authenticated user
        serializer.save(user=self.request.user)