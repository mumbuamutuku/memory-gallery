from django.contrib.auth import get_user_model, authenticate, login
from rest_framework import generics, permissions, status
from rest_framework.decorators import permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.db import IntegrityError
from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from django.shortcuts import render
from django.urls import reverse
from .models import CustomUserManager, CustomUser, UserProfile
from .serializers import CustomUserSerializer, UserProfileSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404

User = get_user_model()

class WelcomeAPIView(APIView):
    """
    API endpoint that provides a welcome message.
    """
    def get(self, request):
        context = {
            'message': 'Welcome to the Memory Gallery!',
        }
        return render(request, 'index.html', context)

class RegistrationAPIView(APIView):
    """
    API endpoint that allows user registration.

    - To register a new user, send a POST request with user data.

    When registering a new user, provide the following data in the request body:
    - `username` (string): The username for the new user.
    - `email` (string): The email address for the new user.
    - `password` (string): The password for the new user.

    Example POST data:
    ```
    {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "secretpassword"
    }
    ```

    Returns a JSON response with the user data upon successful registration.
    """
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
    """
    API endpoint that allows user login.

    - To log in a user, send a POST request with the user's credentials.

    Example POST data:
    ```
    {
        "username": "yourusername",
        "password": "yourpassword"
    }
    ```

    Returns a JSON response with a user token and user data upon successful login.
    """
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
    """
    API endpoint that allows viewing, updating, or deleting user profiles.

    - To view a user profile, send a GET request.
    - To update a user profile, send a PUT request with updated data.
    - To delete a user profile, send a DELETE request.

    Returns a JSON response with user profile data upon successful operations.
    """
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

class EditProfileView(APIView):
    """
    API endpoint that allows viewing and updating user profiles.

    - To view a user profile, send a GET request.
    - To update a user profile, send a PUT request with updated data.

    Returns a JSON response with user profile data upon successful operations.
    """
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

