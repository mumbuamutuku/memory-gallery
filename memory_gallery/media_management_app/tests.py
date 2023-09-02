from django.test import TestCase
from django.urls import reverse
from .models import Album, Media
from .forms import AlbumForm, MediaForm
from django.contrib.auth.models import User

class AlbumModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test album
        self.album = Album.objects.create(
            title='Test Album',
            description='This is a test album.',
            created_by=self.user  # Link the album to the test user
        )

    def test_album_creation(self):
        """
        Test that an album is created correctly.
        """
        self.assertEqual(self.album.title, 'Test Album')
        self.assertEqual(self.album.description, 'This is a test album.')
        self.assertEqual(self.album.created_by, self.user)

class MediaModelTestCase(TestCase):
    def setUp(self):
        # Create a test user (if you're using user authentication)
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test album
        self.album = Album.objects.create(
            title='Test Album',
            description='This is a test album.',
            created_by=self.user
        )

        # Create a test media file
        self.media = Media.objects.create(
            title='Test Media',
            description='This is a test media file.',
            album=self.album,  # Associate the media with the test album
            uploader=self.user  # Link the uploader to the test user
        )

    def test_media_creation(self):
        """
        Test that a media file is created correctly.
        """
        self.assertEqual(self.media.title, 'Test Media')
        self.assertEqual(self.media.description, 'This is a test media file.')
        self.assertEqual(self.media.album, self.album)
        self.assertEqual(self.media.uploader, self.user)

class AlbumListViewTestCase(TestCase):
    def test_album_list_view(self):
        """
        Test the album list view.
        """
        response = self.client.get(reverse('media_management_app:album_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media_management_app/album_list.html')

class AlbumDetailViewTestCase(TestCase):
    def setUp(self):
        # Create a test user (if you're using user authentication)
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test album
        self.album = Album.objects.create(
            title='Test Album',
            description='This is a test album.',
            created_by=self.user
        )

    def test_album_detail_view(self):
        """
        Test the album detail view.
        """
        response = self.client.get(reverse('media_management_app:album_detail', args=[self.album.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media_management_app/album_detail.html')

class CreateAlbumViewTestCase(TestCase):
    def test_create_album_view(self):
        """
        Test the create album view.
        """
        response = self.client.get(reverse('media_management_app:create_album'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media_management_app/create_album.html')

    def test_create_album_form_valid(self):
        """
        Test that a valid album creation form is processed correctly.
        """
        data = {'title': 'New Album', 'description': 'This is a new album.'}
        form = AlbumForm(data=data)
        self.assertTrue(form.is_valid())

    def test_create_album_form_invalid(self):
        """
        Test that an invalid album creation form is not processed.
        """
        data = {'title': '', 'description': ''}  # Invalid data with empty fields
        form = AlbumForm(data=data)
        self.assertFalse(form.is_valid())

class UploadMediaViewTestCase(TestCase):
    def setUp(self):
        # Create a test user (if you're using user authentication)
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test album
        self.album = Album.objects.create(
            title='Test Album',
            description='This is a test album.',
            created_by=self.user
        )

    def test_upload_media_view(self):
        """
        Test the upload media view.
        """
        response = self.client.get(reverse('media_management_app:upload_media', args=[self.album.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media_management_app/upload_media.html')

    def test_upload_media_form_valid(self):
        """
        Test that a valid media upload form is processed correctly.
        """
        data = {'title': 'New Media', 'description': 'This is a new media file.'}
        form = MediaForm(data=data)
        self.assertTrue(form.is_valid())

    def test_upload_media_form_invalid(self):
        """
        Test that an invalid media upload form is not processed.
        """
        data = {'title': '', 'description': ''}  # Invalid data with empty fields
        form = MediaForm(data=data)
        self.assertFalse(form.is_valid())
