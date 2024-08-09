import email
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from authentication.models import User

class UserRegisterTestCase(TestCase):
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
    
    def test_user_required_fields_missing_register(self):
        data = {
            'email': 'WqKQ7@example.com',
            'nickname': 'test',
            'first_name': 'test',
            'last_name':"text",
            'password': 'test123',
            'passwordConfirm': 'test123'
        }
        
        copy_data = data.copy()
        copy_data.pop('email')
        
        response = self.client.post(reverse('user_register'), copy_data)
        
        assert response.status_code == 400
        assert response.data["email"] == ["This field is required."]
        
        copy_data = data.copy()
        copy_data.pop('nickname')
        
        response = self.client.post(reverse('user_register'), copy_data)
        
        assert response.status_code == 400
        assert response.data["nickname"] == ["This field is required."]
        
        copy_data = data.copy()
        copy_data.pop('first_name')
        
        response = self.client.post(reverse('user_register'), copy_data)
        
        assert response.status_code == 400
        assert response.data["first_name"] == ["This field is required."]
        
        copy_data = data.copy()
        copy_data.pop('last_name')
        
        response = self.client.post(reverse('user_register'), copy_data)
        
        assert response.status_code == 400
        assert response.data["last_name"] == ["This field is required."]
        
        copy_data = data.copy()
        copy_data.pop('password')
        
        response = self.client.post(reverse('user_register'), copy_data)
        
        assert response.status_code == 400
        assert response.data["password"] == ["This field is required."]
        
        copy_data = data.copy()
        copy_data.pop('passwordConfirm')
        
        response = self.client.post(reverse('user_register'), copy_data)
        
        assert response.status_code == 400
        assert response.data["passwordConfirm"] == ["This field is required."]
        
        
    def test_user_blank_fields_register(self):
        data = {
            'email': '',
            'nickname': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'password': 'test123',
            'passwordConfirm': 'test123'
        }
        
        copy_data = data.copy()
        copy_data['email'] = ''
        
        response = self.client.post(reverse('user_register'), copy_data)
        
        assert response.status_code == 400
        assert response.data["email"] == ["This field may not be blank."]
        
        copy_data = data.copy()
        copy_data['nickname'] = ''
        
        response = self.client.post(reverse('user_register'), copy_data)
        
        assert response.status_code == 400
        assert response.data["nickname"] == ["This field may not be blank."]
        
        copy_data = data.copy()
        copy_data['first_name'] = ''
        
        response = self.client.post(reverse('user_register'), copy_data)
        
        assert response.status_code == 400
        assert response.data["first_name"] == ["This field may not be blank."]
        
        copy_data = data.copy()
        copy_data['last_name'] = ''
        
        response = self.client.post(reverse('user_register'), copy_data)
        
        assert response.status_code == 400
        assert response.data["last_name"] == ["This field may not be blank."]
        
        copy_data = data.copy()
        copy_data['password'] = ''
        
        response = self.client.post(reverse('user_register'), copy_data)
        
        assert response.status_code == 400
        assert response.data["password"] == ["This field may not be blank."]
        
        copy_data = data.copy()
        copy_data['passwordConfirm'] = ''
        
        response = self.client.post(reverse('user_register'), copy_data)
        
        assert response.status_code == 400
        assert response.data["passwordConfirm"] == ["This field may not be blank."]
        
    
    def test_user_passwords_dont_match_register(self):
        data = {
            'email': 'WqKQ7@example.com',
            'nickname': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'password': 'test123',
            'passwordConfirm': 'test1234'
        }
        
        response = self.client.post(reverse('user_register'), data)
        
        assert response.status_code == 400
        assert response.data["non_field_errors"] == ["Passwords do not match"]
    
    
    