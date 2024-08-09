import pyotp
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

from authentication.utils import send_otp_email, verify_otp_code
class VerifyAccountView(GenericViewSet):
    
    def send_otp_code(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            print(user.secret)
            if not user.secret:
                user.secret = pyotp.random_base32()
                user.save()

            send_otp_email(user.email, user.secret)
            
            return Response(data={'message': "OTP code sent successfully!"}, status=status.HTTP_200_OK) # type: ignore
            
            
    def verify_otp(self, request, otp, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data={'detail': "User not authenticated!"}, status=status.HTTP_401_UNAUTHORIZED) # type: ignore
        
        user = request.user
        if user.is_verified:
            return Response(data={'message': "User already verified!"}, status=status.HTTP_400_BAD_REQUEST) # type: ignore
            
        if not user.secret:
            user.secret = pyotp.random_base32()
            user.save()
            
        if verify_otp_code(otp, user.secret):
            user.is_verified = True
            user.save()
            return Response(data={'message': "User verified successfully!"}, status=status.HTTP_200_OK) # type: ignore
            
        return Response(data={'detail': "Invalid OTP code!"}, status=status.HTTP_400_BAD_REQUEST) # type: ignore