from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom user model.

    This serializer is used for user registration.

    Fields:
    - `id` (read-only): The unique identifier for the user.
    - `email` (string): The email address for the user.
    - `username` (string): The username for the user.
    - `password` (string, write-only): The password for the user.

    To create a new user, provide the following data in the serializer:
    - `email`: The email address for the new user.
    - `username`: The username for the new user.
    - `password`: The password for the new user.

    Example usage:
    ```json
    {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "secretpassword"
    }
    ```

    The `id` field is automatically generated upon user creation.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profiles.

    This serializer is used to retrieve and update user profile information.

    Fields:
    - `username` (read-only): The username associated with the user profile.
    - `email` (read-only): The email address associated with the user profile.
    - `profile_picture` (image): The user's profile picture (if available).
    - `bio` (string): The user's biography or description.

    The `username` and `email` fields are read-only and derived from the associated user.
    """
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'profile_picture', 'bio')



