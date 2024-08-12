from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from authentication.models.user import User

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        
        if email is None or email == '':
            return Response({'error': 'Email not provided!'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)
        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)
        reset_url = f"{request.build_absolute_uri('/')}reset-password/{uid}/{token}" #f'http://localhost:3000/reset-password/{uid}/{token}'
        
        send_mail(
            'Password Reset Request',
            f'Click the link below to reset your password: {reset_url}',
            '4OZsG@example.com',
            [email],
            fail_silently=False
        )
        
        return Response({'message': 'Password reset email sent!'}, status=status.HTTP_200_OK)