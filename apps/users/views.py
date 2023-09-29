from django.contrib.auth import get_user_model, authenticate, login
from rest_framework import generics, permissions, status
from rest_framework.decorators import permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from django.shortcuts import render, redirect
from django.urls import reverse
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
    serializer_class = CustomUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # Check if the email or username already exists
            if CustomUser.objects.filter(email=email).exists():
                return Response({'detail': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

            if CustomUser.objects.filter(username=username).exists():
                return Response({'detail': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

            # Create the user (CustomUser)
            user = serializer.save()
            user.set_password(password)
            user.save()

            try:
                # Create the user profile with the user instance
                UserProfile.objects.create(user=user)
            except IntegrityError:
                # Handle errors in profile creation, if any
                user.delete()  # Delete the user if profile creation fails
                return Response({'detail': 'Failed to create user profile'}, status=status.HTTP_400_BAD_REQUEST)

            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                user_data = {
                   'user_id': user.id,
                   'username': user.username,
                   'email': user.email,
                }

                return Response(user_data, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': 'Failed to authenticate user'}, status=status.HTTP_400_BAD_REQUEST)

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
               'token': token.key,  # Add the user token
               'user_id': user.id,
               'username': user.username,
               'email': user.email,
            }
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileAPIView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
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

#class CreateProfileView(generics.CreateAPIView):
 #   queryset = UserProfile.objects.all()
  #  serializer_class = UserProfileSerializer

   # def perform_create(self, serializer):
        # Automatically set the user field to the currently authenticated user
    #    serializer.save(user=self.request.user)


class EditProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        # Retrieve the user's profile
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    def put(self, request):
        # Retrieve the user's profile
        user_profile = UserProfile.objects.get(user=request.user)

        # Deserialize the updated data
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


