from rest_framework import serializers
from .models import Album, Memory

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('id', 'title', 'description', 'cover_photo', 'date_created', 'user', 'memories')

class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = ('id', 'caption', 'image', 'video', 'date', 'user', 'album')

    def create(self, validated_data):
        user = self.context['request'].user
        album = validated_data.pop('album', None)  # Remove 'album' from validated_data if present
        memory = Memory.objects.create(user=user, **validated_data)

        # If 'album' was provided in the request, associate the memory with the album
        if album:
            memory.album = album
            memory.save()

        return memory
