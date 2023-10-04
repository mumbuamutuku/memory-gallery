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
        fields = ('id', 'caption', 'image', 'video', 'date', 'user', 'albums')

    def create(self, validated_data: dict) -> Memory:
        """
        Create a new Memory instance.

        Args:
            validated_data (dict): Validated data for Memory creation.

        Returns:
            Memory: The newly created Memory instance.
        """
        album_ids = validated_data.pop('albums', None)

        user: Optional[User] = self.context.get('request').user if 'request' in self.context else None

        if 'user' not in validated_data:
            validated_data['user'] = user

        memory = Memory.objects.create(**validated_data)

        if album_ids:
            albums = Album.objects.filter(id__in=album_ids, user=user)
            memory.albums.set(albums)

        return memory

