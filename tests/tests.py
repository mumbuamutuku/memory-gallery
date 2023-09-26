from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from apps.users.models import CustomUser
from apps.users.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.registration_url = reverse('user-register')
        self.valid_payload = {
            'email': 'abakpad82@gmail.com',
            'username': 'Abakpa',
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

class UserProfileAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='Dominic', email='abakpad82@gmail.com', password='SV07Elversberg')
        #self.user_profile_url = reverse('user-profile')
        self.user_profile_url = reverse('user-profile', args=[3])
        self.client.login(email='abakpad82@gmail.com', password='SV07Elversberg')

    def test_get_user_profile(self):
        response = self.client.get(self.user_profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_profile(self):
        payload = {
            'profile_picture': None,
            'bio': 'This is Mumbua doing test case',
        }
        response = self.client.put(self.user_profile_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(updated_user_profile.profile_picture, None)
        self.assertEqual(updated_user_profile.bio, 'This is Mumbua doing test case')

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get(self.user_profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
class UserProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='Dominic',
            email='abakpad82@gmail.com',
            password='SV07Elversberg'
        )

    def test_user_profile_creation(self):
        # Create a UserProfile associated with the user
        user_profile = UserProfile.objects.create(
            user=self.user,
            profile_picture=None,  # Set it explicitly to None
            bio='Hey guys, Mumbua here'
        )

         # Retrieve the user profile from the database
        retrieved_profile = UserProfile.objects.get(user=self.user)

        # Verify that the created user profile matches the retrieved one
        self.assertEqual(user_profile, retrieved_profile)
        self.assertEqual(user_profile.user, self.user)
        self.assertEqual(user_profile.bio, 'Hey guys, Mumbua here')
    
        # Check if profile_picture is either None or an empty string
        self.assertTrue(user_profile.profile_picture in (None, ''))
        
    def test_user_profile_str_representation(self):
        # Create a UserProfile associated with the user
        user_profile = UserProfile.objects.create(
            user=self.user,
            profile_picture=None,
            bio='Hey guys, Mumbua here'
        )

        # Verify that the string representation of UserProfile is the user's email
        self.assertEqual(str(user_profile), 'abakpad82@gmail.com')
