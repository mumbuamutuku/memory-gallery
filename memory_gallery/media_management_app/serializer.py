from rest_framework import serializers
from .models import Album, Media

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('id', 'title', 'description', 'created_by', 'created_at')

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ('id', 'title', 'description', 'album', 'uploader', 'upload_date', 'privacy_setting', 'file')
