from rest_framework import viewsets, permissions
from .models import Album, Media
from .serializers import AlbumSerializer, MediaSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires authentication for all album actions

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires authentication for all media actions

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)

    def list(self, request, album_id=None):
        # Retrieve all media items for a specific album
        queryset = Media.objects.filter(album=album_id)
        serializer = MediaSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, album_id=None, pk=None):
        # Retrieve a single media item within a specific album
        queryset = Media.objects.filter(album=album_id)
        media = get_object_or_404(queryset, pk=pk)
        serializer = MediaSerializer(media)
        return Response(serializer.data)
