from rest_framework import serializers
from .models import Album, Memory
from typing import Optional
from django.contrib.auth.models import User

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('id', 'title', 'description', 'cover_photo', 'date_created', 'user')

class MemorySerializer(serializers.ModelSerializer):
    """
    Serializer for Memory model.

    Attributes:
        create: Creates a new Memory instance.
    """

    class Meta:
        model = Memory
        fields = ('id', 'caption', 'image', 'video', 'date', 'user', 'album')

    def create(self, validated_data: dict) -> Memory:
        """
        Create a new Memory instance.

        Args:
            validated_data (dict): Validated data for Memory creation.

        Returns:
            Memory: The newly created Memory instance.
        """
        user: Optional[User] = self.context.get('request').user if 'request' in self.context else None

        if 'user' not in validated_data:
            validated_data['user'] = user

        # Assuming you have an 'album_id' field in the request data to specify the album
        album_id = validated_data.pop('album_id', None)

        if album_id:
            album = Album.objects.get(id=album_id, user=user)
            validated_data['album'] = album

        memory = Memory.objects.create(**validated_data)
        return memory
