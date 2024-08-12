

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.core import mail


class TestResetPasswordRequest(TestCase):

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
        self.email = data['email']
    
    def test_reset_password_request_email(self):
        response = self.client.post(reverse('password_reset_request'), {'email': self.email})
        
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.data['message'], 'Password reset email sent!')
        
        self.assertEqual(len(mail.outbox), 1)
        
        self.assertEqual(mail.outbox[0].subject, 'Password Reset Request')
    
    def test_reset_password_request_email_not_found(self):
        response = self.client.post(reverse('password_reset_request'), {'email': 'WqKQ713@example.com'})
        
        self.assertEqual(response.status_code, 404)
        
        self.assertEqual(response.data['error'], 'User not found!')
    
    def test_reset_password_request_email_blank(self):
        response = self.client.post(reverse('password_reset_request'), {'email': ''})
        
        self.assertEqual(response.status_code, 400)
        
        self.assertEqual(response.data['error'], 'Email not provided!')
        
        response = self.client.post(reverse('password_reset_request'))
        
        self.assertEqual(response.status_code, 400)
        
        self.assertEqual(response.data['error'], 'Email not provided!')
        
        