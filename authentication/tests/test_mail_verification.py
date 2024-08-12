

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.core import mail


class MailVerificationTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        user_data = {
            'email': 'WqKQ7@example.com',
            'nickname': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'password': 'test123',
            'passwordConfirm': 'test123'
        }
        
        response_register = self.client.post(reverse('user_register'), user_data)
        self.tokens = response_register.data
        
    def test_mail_sent(self):
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.tokens['access'])
        
        response = self.client.post(reverse('send_otp_code'))
        
        assert response.status_code == 200
        
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Your verification code')
    
    def test_mail_verification_sucessfuly(self):
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.tokens['access'])
        
        response = self.client.post(reverse('send_otp_code'))
        
        assert response.status_code == 200
        
        otp = int(mail.outbox[0].body.split(" ")[-1])
        
        response = self.client.get(reverse('verify_otp', kwargs={'otp': otp}))
        
        assert response.status_code == 200
        assert response.data["message"] == "User verified successfully!"
    
    def test_mail_verification_failed(self):
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.tokens['access'])
        
        otp = 135691
        
        response = self.client.get(reverse('verify_otp', kwargs={'otp': otp}))
        
        assert response.status_code == 400
        assert response.data["detail"] == "Invalid OTP code!"