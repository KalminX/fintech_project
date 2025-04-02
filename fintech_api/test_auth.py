from .models import CustomUser
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser


class AuthTestCase(APITestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.user_data = {
            'first_name': 'kalmin',
            'last_name': 'numzy',
            'email': 'kalmin@gmail.com',
            'password': 'kally123'
        }
    
    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertIn('access', response.data)
    
    def test_register_existing_user(self):
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertIn('error', response.data)

    def test_user_login(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_data = {
            'email': 'kalmin@gmail.com',
            'password': 'kally123'
        }
        response = self.client.post(self.login_url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
    
    def test_user_login_with_wrong_details(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_data = {
            'email': 'kalmin@gmail.com',
            'password': 'kally123!'
        }
        response = self.client.post(self.login_url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotIn('access', response.data)