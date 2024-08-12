from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication.models.user import User

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    
    class InputSerializer(serializers.Serializer):
        uidb64 = serializers.CharField()
        token = serializers.CharField()
        new_password = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uidb64 = serializer.validated_data.get('uidb64')
        token = serializer.validated_data.get('token')
        new_password = serializer.validated_data.get('new_password')

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if not user or not PasswordResetTokenGenerator().check_token(user, token):
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password reset successful!'}, status=status.HTTP_200_OK)