from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock

User = get_user_model()


class UserTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com',password='securepassword')

    def test_user_registration(self):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')

    def test_user_login(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'securepassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Login successful')

    def test_user_update(self):
        url = reverse('user-detail', kwargs={'pk': self.user.id})
        self.client.login(username='testuser', password='securepassword')
        data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'password': 'newsecurepassword'  # Note that password is not updated here; modify as necessary
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_user_delete(self):
        url = reverse('user-detail', kwargs={'pk': self.user.id})
        self.client.login(username='testuser', password='securepassword')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CustomUser.objects.filter(id=self.user.id).exists())  # Verify user no longer exists



class SocialAuthenticationTests(TestCase):
    def setUp(self):
        # Setup test client and common test data
        self.client = APIClient()
        self.google_login_url = reverse('google_signin')
        self.apple_login_url = reverse('apple_signin')

    def test_google_signin_new_user(self):
        # Mock the Google token verification
        with patch('google.oauth2.id_token.verify_firebase_token') as mock_verify:
            # Setup mock return value for token verification
            mock_verify.return_value = {
                'email': 'newuser@gmail.com',
                'name': 'Test User',
            }

            # Prepare test data
            payload = {
                'id_token': 'mock_google_token'
            }

            # Make the request
            response = self.client.post(self.google_login_url, payload, format='json')

            # Assertions
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['message'], 'Google Login successful')
            self.assertTrue(response.data['created'])
            
            # Verify user was created
            user = User.objects.get(email='newuser@gmail.com')
            self.assertIsNotNone(user)
            self.assertEqual(user.username, 'newuser@gmail.com')

    def test_google_signin_existing_user(self):
        # Create an existing user
        existing_user = User.objects.create_user(
            username='existinguser@gmail.com',
            email='existinguser@gmail.com',
            password='testpass123'
        )

        # Mock the Google token verification
        with patch('google.oauth2.id_token.verify_firebase_token') as mock_verify:
            # Setup mock return value for token verification
            mock_verify.return_value = {
                'email': 'existinguser@gmail.com',
                'name': 'Existing User',
            }

            # Prepare test data
            payload = {
                'id_token': 'mock_google_token'
            }

            # Make the request
            response = self.client.post(self.google_login_url, payload, format='json')

            # Assertions
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['message'], 'Google Login successful')
            self.assertEqual(response.data['user'], 'existinguser@gmail.com')
            self.assertFalse(response.data['created'])

    def test_apple_signin_new_user(self):
        # Mock the Firebase token verification
        with patch('firebase_admin.auth.verify_id_token') as mock_verify:
            # Setup mock return value for token verification
            mock_verify.return_value = {
                'email': 'newappleuser@example.com',
                'uid': 'apple_unique_id_123'
            }

            # Prepare test data
            payload = {
                'id_token': 'mock_apple_token'
            }

            # Make the request
            response = self.client.post(self.apple_login_url, payload, format='json')

            # Assertions
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['message'], 'Apple Login successful')
            self.assertTrue(response.data['created'])
            
            # Verify user was created
            user = User.objects.get(email='newappleuser@example.com')
            self.assertIsNotNone(user)
            self.assertEqual(user.username, 'apple_apple_unique_id_123')

    def test_apple_signin_existing_user(self):
        # Create an existing user
        existing_user = User.objects.create_user(
            username='existingappleuser@example.com',
            email='existingappleuser@example.com',
            password='testpass123'
        )

        # Mock the Firebase token verification
        with patch('firebase_admin.auth.verify_id_token') as mock_verify:
            # Setup mock return value for token verification
            mock_verify.return_value = {
                'email': 'existingappleuser@example.com',
                'uid': 'apple_existing_id'
            }

            # Prepare test data
            payload = {
                'id_token': 'mock_apple_token'
            }

            # Make the request
            response = self.client.post(self.apple_login_url, payload, format='json')

            # Assertions
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['message'], 'Apple Login successful')
            self.assertEqual(response.data['user'], 'existingappleuser@example.com')
            self.assertFalse(response.data['created'])

    def test_google_signin_invalid_token(self):
        # Mock the Google token verification to raise an error
        with patch('google.oauth2.id_token.verify_firebase_token') as mock_verify:
            # Simulate token verification failure
            mock_verify.side_effect = ValueError('Invalid token')

            # Prepare test data
            payload = {
                'id_token': 'invalid_token'
            }

            # Make the request
            response = self.client.post(self.google_login_url, payload, format='json')

            # Assertions
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid token', str(response.data))

    def test_apple_signin_invalid_token(self):
        # Mock the Firebase token verification to raise an error
        with patch('firebase_admin.auth.verify_id_token') as mock_verify:
            # Simulate token verification failure
            from firebase_admin import auth as firebase_auth
            mock_verify.side_effect = firebase_auth.InvalidIdTokenError('Invalid token')

            # Prepare test data
            payload = {
                'id_token': 'invalid_token'
            }

            # Make the request
            response = self.client.post(self.apple_login_url, payload, format='json')

            # Assertions
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid token', str(response.data))

    def test_missing_token(self):
        # Test Google Sign-in without token
        response_google = self.client.post(self.google_login_url, {}, format='json')
        self.assertEqual(response_google.status_code, 400)
        self.assertEqual(response_google.data['error'], 'ID token is required')

        # Test Apple Sign-in without token
        response_apple = self.client.post(self.apple_login_url, {}, format='json')
        self.assertEqual(response_apple.status_code, 400)
        self.assertEqual(response_apple.data['error'], 'ID token is required')