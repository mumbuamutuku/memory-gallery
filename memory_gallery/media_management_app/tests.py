from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Album, Media

class MediaManagementTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create some test albums
        self.album1 = Album.objects.create(title='Album 1', description='Description 1', created_by=self.user)
        self.album2 = Album.objects.create(title='Album 2', description='Description 2', created_by=self.user)

        # Create a test media item
        self.media = Media.objects.create(
            title='Media Item',
            description='Media Description',
            album=self.album1,
            uploader=self.user,
            privacy_setting='public'
        )

        # Create an API client for making requests
        self.client = APIClient()

    def test_create_album(self):
        # Test creating a new album
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        album_count = Album.objects.count()
        new_album_data = {'title': 'New Album', 'description': 'New Description'}
        response = self.client.post('/api/albums/', new_album_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Album.objects.count(), album_count + 1)

    def test_create_media(self):
        # Test creating a new media item
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        media_count = Media.objects.count()
        new_media_data = {
            'title': 'New Media',
            'description': 'New Media Description',
            'album': self.album2.id,
            'privacy_setting': 'public'
        }
        response = self.client.post('/api/media/', new_media_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Media.objects.count(), media_count + 1)

    def test_list_albums(self):
        # Test listing albums
        response = self.client.get('/api/albums/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_media(self):
        # Test listing media items
        response = self.client.get('/api/media/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
