from .models import CustomUser
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser


class AuthTestCase(APITestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.two_factor_enable = reverse('2fa-enable')
        self.two_factor_disable = reverse('2fa-disable')
        self.generate_otp_url = reverse('generate-otp')
        self.verify_otp_url = reverse('verify-otp')
        self.user_data = {
            'first_name': 'kalmin',
            'last_name': 'numzy',
            'email': 'kalmin@gmail.com',
            'password': 'kally123',
            'two_factor_enabled': False
        }
    
    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertIn('access', response.data)
        user = CustomUser.objects.get(user_id=response.data['user_id'])
        self.assertIsNotNone(user.otp_base32)

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
    
    def test_user_2fa_login(self):
        user_data = {
            'first_name': 'kalmin',
            'last_name': 'numzy',
            'email': 'kalmin@gmail.com',
            'password': 'kally123',
            'two_factor_enabled': True
        }
        response = self.client.post(self.register_url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_data = {
            'email': 'kalmin@gmail.com',
            'password': 'kally123'
        }
        response = self.client.post(self.login_url, user_data, format='json')
        self.assertTrue(response.data['two_factor_enabled'])
    
    def test_enable_two_fa(self):
        user_data = {
            'first_name': 'kalmin',
            'last_name': 'numzy',
            'email': 'kalmin@gmail.com',
            'password': 'kally123'
        }
        response = self.client.post(self.register_url, user_data, format='json')
        two_factor_response = self.client.post(self.two_factor_enable, {'user_id': response.data['user_id']})
        self.assertTrue(two_factor_response.data['two_factor_enabled'])
    
    def test_disable_two_fa(self):
        user_data = {
            'first_name': 'kalmin',
            'last_name': 'numzy',
            'email': 'kalmin@gmail.com',
            'password': 'kally123',
            'two_factor_enabled': True
        }
        response = self.client.post(self.register_url, user_data, format='json')
        two_factor_response = self.client.post(self.two_factor_disable, {'user_id': response.data['user_id']})
        self.assertFalse(two_factor_response.data['two_factor_enabled'])
    
    #################### Tests for 2fa #############################
    def test_enable_two_fa_if_already_enabled(self):
        user_data = {
            'first_name': 'kalmin',
            'last_name': 'numzy',
            'email': 'kalmin@gmail.com',
            'password': 'kally123',
            'two_factor_enabled': True
        }
        response = self.client.post(self.register_url, user_data, format='json')
        two_factor_response = self.client.post(self.two_factor_enable, {'user_id': response.data['user_id']})
        self.assertIn('message', two_factor_response.data)
    
    def test_generate_otp(self):
        user_data = {
            'first_name': 'kalmin',
            'last_name': 'numzy',
            'email': 'kalmin@gmail.com',
            'password': 'kally123',
            'two_factor_enabled': True
        }
        response = self.client.post(self.register_url, user_data, format='json')
        generate_otp_response = self.client.post(self.generate_otp_url, {'user_id': response.data['user_id']}, format='json')
        self.assertIsNotNone(generate_otp_response.data['code'])
        self.assertIsNotNone(generate_otp_response.data['otp_url'])
    
    def test_verify_correct_otp(self):
        user_data = {
            'first_name': 'kalmin',
            'last_name': 'numzy',
            'email': 'kalmin@gmail.com',
            'password': 'kally123',
            'two_factor_enabled': True
        }
        response = self.client.post(self.register_url, user_data, format='json')
        generate_otp_response = self.client.post(self.generate_otp_url, {'user_id': response.data['user_id']}, format='json')
        self.assertIsNotNone(generate_otp_response.data['code'])
        payload = {
            'user_id': response.data['user_id'],
            'code': generate_otp_response.data['code']
        }
        response = self.client.post(self.verify_otp_url, payload, format='json')
        self.assertTrue(response.data['valid'])
    
    def test_verify_wrong_otp(self):
        user_data = {
            'first_name': 'kalmin',
            'last_name': 'numzy',
            'email': 'kalmin@gmail.com',
            'password': 'kally123',
            'two_factor_enabled': True
        }
        response = self.client.post(self.register_url, user_data, format='json')
        generate_otp_response = self.client.post(self.generate_otp_url, {'user_id': response.data['user_id']}, format='json')
        self.assertIsNotNone(generate_otp_response.data['code'])
        payload = {
            'user_id': response.data['user_id'],
            'code': '123456'
        }
        response = self.client.post(self.verify_otp_url, payload, format='json')
        self.assertFalse(response.data['valid'])
