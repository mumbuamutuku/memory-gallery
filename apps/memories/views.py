from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FileUploadParser
from .models import Album, Memory
from .serializers import AlbumSerializer, MemorySerializer
from apps.users.models import CustomUser

class AlbumListCreateView(generics.ListCreateAPIView):
    """
    List and create albums.

    This view allows authenticated users to list their albums or create new ones.
    Albums are collections that can store memories.

    GET: List all albums owned by the authenticated user.
    POST: Create a new album.

    When creating a new album, provide the following data:
    - `title` (string): The title of the album (required).
    - `description` (string, optional): A description of the album.
    - `cover_photo` (image file, optional): The cover photo for the album.

    Example POST request data:
    ```json
    {
        "title": "Vacation 2023",
        "description": "Memories from our vacation in 2023",
        "cover_photo": (file)
    }
    ```

    The `cover_photo` field accepts an image file.

    When listing albums, the response will contain a list of albums with their details.
    """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request):
        albums = Album.objects.filter(user=request.user)
        serializer = AlbumSerializer(albums, many=True)
        return Response({'albums': serializer.data}, status=status.HTTP_200_OK)

class AlbumDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete an album.

    This view allows authenticated users to retrieve, update, or delete their albums.

    GET: Retrieve details of an album.
    PUT: Update an album's details.
    DELETE: Delete an album.

    To update an album, provide the following data in the request body:
    - `title` (string, optional): The new title of the album.
    - `description` (string, optional): The new description of the album.
    - `cover_photo` (image file, optional): The new cover photo for the album.

    Example PUT request data to update the album title:
    ```json
    {
        "title": "New Vacation 2023"
    }
    ```

    DELETE request will remove the album and its associated memories.
    """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]

class MemoryListCreateView(APIView):
    """
    List and create memories.

    This view allows authenticated users to list their memories or create new ones.

    GET: List all memories owned by the authenticated user.
    POST: Create a new memory.

    When creating a new memory, provide the following data:
    - `caption` (string, optional): A caption for the memory.
    - `image` (image file, optional): An image for the memory.
    - `video` (video file, optional): A video for the memory.
    - `albums` (list of album IDs, optional): A list of album IDs to associate the memory with.

    Example POST request data to create a memory with an image:
    ```json
    {
        "caption": "Beautiful sunset",
        "image": (file),
        "albums": [1, 2]
    }
    ```

    The `albums` field accepts a list of album IDs to associate the memory with.

    When listing memories, the response will contain a list of memories with their details.
    """
    parser_classes = (MultiPartParser,)

    def get(self, request):
        memories = Memory.objects.filter(user=request.user)
        serializer = MemorySerializer(memories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Pass the user as part of the context
        serializer = MemorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a memory.

    This view allows authenticated users to retrieve, update, or delete their memories.

    GET: Retrieve details of a memory.
    PUT: Update a memory's details.
    DELETE: Delete a memory.

    To update a memory, provide the following data in the request body:
    - `caption` (string, optional): The new caption for the memory.
    - `image` (image file, optional): The new image for the memory.
    - `video` (video file, optional): The new video for the memory.
    - `albums` (list of album IDs, optional): A list of album IDs to associate the memory with.

    Example PUT request data to update the memory caption:
    ```json
    {
        "caption": "Amazing beach sunset"
    }
    ```

    DELETE request will remove the memory.
    """
    queryset = Memory.objects.all()
    serializer_class = MemorySerializer
    permission_classes = [permissions.IsAuthenticated]

class MemoriesByAlbumView(generics.ListAPIView):
    serializer_class = MemorySerializer

    def get_queryset(self):
        album_id = self.kwargs.get('album_id')
        return Memory.objects.filter(album__id=album_id)
