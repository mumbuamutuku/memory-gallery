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
        user = self.context.get('request').user if 'request' in self.context else None
        album_ids = validated_data.pop('albums', None)  # Remove albums from validated data
        memory = Memory.objects.create(user=user, **validated_data)

        # If album IDs are provided in the request data, associate the memory with the albums
        if album_ids:
            albums = Album.objects.filter(id__in=album_ids, user=user)
            memory.albums.set(albums)

        return memory

