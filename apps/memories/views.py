from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FileUploadParser
from .models import Album, Memory
from .serializers import AlbumSerializer, MemorySerializer
from apps.users.models import CustomUser  # Import the custom user model from the users app

class AlbumListCreateView(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AlbumDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]

class MemoryListCreateView(APIView):
    parser_classes = (MultiPartParser,)

    def get(self, request):
        memories = Memory.objects.filter(user=request.user)
        serializer = MemorySerializer(memories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MemorySerializer(data=request.data)
        if serializer.is_valid():
            # Check if 'album' field exists in request data
            if 'album' in request.data:
                album_id = request.data['album']
                try:
                    album = Album.objects.get(id=album_id, user=request.user)
                    serializer.save(user=request.user, album=album)
                except Album.DoesNotExist:
                    return Response({'detail': 'Album not found'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MemoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Memory.objects.all()
    serializer_class = MemorySerializer
    permission_classes = [permissions.IsAuthenticated]

