from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from .models import CustomUser

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
