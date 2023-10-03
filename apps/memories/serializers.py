from rest_framework import serializers
from .models import Album, Memory

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('id', 'title', 'description', 'cover_photo', 'date_created', 'user')

class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = ('id', 'caption', 'image', 'video', 'date', 'user', 'albums')

    def create(self, validated_data):
        # Get the user from the request context
        request = self.context.get('request')
        user = request.user if request else None

        # Extract the album IDs from the validated data
        album_ids = validated_data.pop('albums', None)

        # Create the memory object
        memory = Memory.objects.create(user=user, **validated_data)

        # If album IDs are provided, associate the memory with the albums
        if album_ids:
            albums = Album.objects.filter(id__in=album_ids, user=user)
            memory.albums.set(albums)

        return memory

