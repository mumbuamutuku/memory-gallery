from rest_framework import serializers
from .models import Album, Memory

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('id', 'title', 'description', 'cover_photo', 'date_created', 'user', 'memories')

class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = ('id', 'title', 'caption', 'image', 'video', 'date', 'user', 'album')

    def create(self, validated_data):
        user = self.context['request'].user
        memory = Memory.objects.create(user=user, **validated_data)
        return memory
