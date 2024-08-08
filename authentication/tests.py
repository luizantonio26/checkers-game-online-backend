import email
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from authentication.models import User

class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register(self):
        data = {
            'email': 'WqKQ7@example.com',
            'nickname': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'password': 'test123',
            'passwordConfirm': 'test123'
        }
        
        response = self.client.post(reverse('user_register'), data)
        
        assert response.status_code == 201
        assert User.objects.all().count() == 1
        assert User.objects.get(email='WqKQ7@example.com')
        assert User.objects.get(email='WqKQ7@example.com').check_password('test123')
        assert response.data["refresh"] is not None
        assert response.data["access"] is not None
    
    
    def test_user_login(self):
        user_data = {
            'email': 'WqKQ7@example.com',
            'nickname': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'password': 'test123',
            'passwordConfirm': 'test123'
        }
        
        response_register = self.client.post(reverse('user_register'), user_data)
        
        user_credentials = {
            'email': 'WqKQ7@example.com',
            'password': 'test123'
        }
        
        response = self.client.post(reverse('user_login'), user_credentials)
        
        assert response.status_code == 200
        assert response.data["refresh"] is not None
        assert response.data["access"] is not None
        
    
    def test_user_required_fields_missing_login(self):
        user_data = {
            'email': 'WqKQ7@example.com',
            'nickname': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'password': 'test123',
            'passwordConfirm': 'test123'
        }
        
        response_register = self.client.post(reverse('user_register'), user_data)
        
        user_credentials = {
            'password': 'test123'
        }
        
        response = self.client.post(reverse('user_login'), user_credentials)
        
        assert response.status_code == 400
        assert response.data["email"] == ["This field is required."]
        
        user_credentials = {
            'email': 'WqKQ7@example.com',
        }
        
        response = self.client.post(reverse('user_login'), user_credentials)
        
        assert response.status_code == 400
        assert response.data["password"] == ["This field is required."]
        
        user_credentials = {
        }
        
        response = self.client.post(reverse('user_login'), user_credentials)
        
        assert response.status_code == 400
        assert response.data["password"] == ["This field is required."]
        assert response.data["email"] == ["This field is required."]
        
        
        
    def test_user_blank_fields_login(self):
        user_data = {
            'email': 'WqKQ7@example.com',
            'nickname': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'password': 'test123',
            'passwordConfirm': 'test123'
        }   
        
        response_register = self.client.post(reverse('user_register'), user_data)
        
        user_credentials = {
            'email': '',
            'password': 'test123'
        }
        
        response = self.client.post(reverse('user_login'), user_credentials)
        
        assert response.status_code == 400
        assert response.data["email"] == ["This field may not be blank."]
        
        user_credentials = {
            'email': 'WqKQ7@example.com',
            'password': ''
        }
        
        response = self.client.post(reverse('user_login'), user_credentials)
        
        assert response.status_code == 400
        assert response.data["password"] == ["This field may not be blank."]
        
        user_credentials = {
            'email': '',
            'password': ''
        }
        
        response = self.client.post(reverse('user_login'), user_credentials)
        
        assert response.status_code == 400
        assert response.data["email"] == ["This field may not be blank."]
        assert response.data["password"] == ["This field may not be blank."]        
    
    def test_user_invalid_credentials(self):
        user_data = {
            'email': 'WqKQ7@example.com',
            'nickname': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'password': 'test123',
            'passwordConfirm': 'test123'
        }
        
        response_register = self.client.post(reverse('user_register'), user_data)
        
        user_credentials = {
            'email': 'WqKQ7@example.com',
            'password': 'test1234'
        }
        
        response = self.client.post(reverse('user_login'), user_credentials)
        
        assert response.status_code == 400
        assert response.data["detail"] == "Invalid credentials"