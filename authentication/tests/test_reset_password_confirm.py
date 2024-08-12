

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.core import mail

from authentication.models.user import User


class TestResetPasswordConfirm(TestCase):

    def setUp(self):
        self.client = APIClient()
        data = {
            "email": "WqKQ7@example.com",
            "nickname": "test",
            "first_name": "test",
            "last_name": "test",
            "password": "test123",
            "passwordConfirm": "test123"
        }
        
        self.client.post(reverse('user_register'), data)
        self.user = User.objects.get(email='WqKQ7@example.com')
        self.password = data['password']
    
    def test_reset_password_confirm(self):
        response = self.client.post(reverse('password_reset_request'), {'email': self.user.email})
        
        self.assertEqual(response.status_code, 200)
        
        url = mail.outbox[0].body.split("Click the link below to reset your password: ")[1]
        uid = url.split("/")[4]
        token = url.split("/")[5]
        new_password='newtest123'
        
        response = self.client.post(reverse('password_reset_confirm'), data={'uidb64': uid, 'token': token, 'new_password': new_password})
        
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.data['message'], 'Password reset successful!')
        
        res = self.client.post(reverse('user_login'), {'email': 'WqKQ7@example.com', 'password': self.password})
        
        self.assertEqual(res.status_code, 400)
        
        res = self.client.post(reverse('user_login'), {'email': 'WqKQ7@example.com', 'password': 'newtest123'})
        
        self.assertEqual(res.status_code, 200)
    
    
        
        