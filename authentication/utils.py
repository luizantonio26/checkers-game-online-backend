import string
from django.core.mail import send_mail
from django.conf import settings
import pyotp

def generate_otp(secret):
    """Gera um OTP com números e letras."""
    code =  pyotp.TOTP(secret, interval=180).now()
    return code

def send_otp_email(user_email, user_secret):
    """Envia um OTP para o email do usuário."""
    otp = generate_otp(secret=user_secret)
    subject = 'Your verification code'
    message = f'Your verification code is: {otp}'
    
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
    
    return otp

def verify_otp_code(code, user_secret):
    """Verifica se o código de verificação é o correto."""
    return pyotp.TOTP(user_secret, interval=180).verify(code)