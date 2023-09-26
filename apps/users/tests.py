from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from .models import CustomUser
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from users.models import UserProfile  # Replace 'your_app' with the actual name of your app


class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.registration_url = reverse('user-register')
        self.valid_payload = {
            'email': 'abakpad82@gmail.com',
            'username': 'Dominic',
            'password': 'SV07Elversberg'
        }

    def test_valid_user_registration(self):
        response = self.client.post(self.registration_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().email, 'abakpad82@gmail.com')

    def test_invalid_user_registration(self):
        # Test with missing required fields
        invalid_payload = {}
        response = self.client.post(self.registration_url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that the response contains errors for missing fields
        self.assertIn('email', response.data)
        self.assertIn('username', response.data)
        self.assertIn('password', response.data)

class UserProfileAPITest(APITestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a user profile associated with the user
        self.user_profile = UserProfile.objects.create(user=self.user, userid='2', email='m@gmail.com')

    def test_get_user_profile(self):
        # Log in as the user
        self.client.login(username='testuser', password='testpassword')

        # Make a GET request to the profile endpoint
        url = '/profile/2/'  # Adjust the URL as needed
        response = self.client.get(url)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data to ensure it matches the expected user profile data
        self.assertEqual(response.data['userid'], '2')
        self.assertEqual(response.data['email'], 'm@gmail.com')
        # Add more assertions for other fields as needed

    def test_get_user_profile_unauthenticated(self):
        # Make a GET request to the profile endpoint without logging in
        url = '/profile/2/'  # Adjust the URL as needed
        response = self.client.get(url)

        # Check if the response status code is 401 (Unauthorized) for unauthenticated users
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
