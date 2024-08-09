from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from authentication.models import User
from authentication.serializers.user_serializer import LoginUserSerializer, RegisterUserSerializer


class UserViewSet(viewsets.GenericViewSet):
    serializer_class = RegisterUserSerializer
    
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            user = serializer.instance
            tokens = user.get_tokens()
            
            return Response(data=tokens, status=status.HTTP_201_CREATED) # type: ignore
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST) # type: ignore

    def login(self, request, *args, **kwargs):
        serializer = LoginUserSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                user = authenticate(**serializer.validated_data) # type: ignore
                
                if not user:
                    return Response(data={'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST) # type: ignore
                
                return Response(data=user.get_tokens(), status=status.HTTP_200_OK) # type: ignore
            except Exception as e:
                return Response(data={'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST) # type: ignore
            
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST) # type: ignore
    
    def authenticated_route_test(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response(data={'authenticated': True}, status=status.HTTP_200_OK) # type: ignore
        return Response(data={'authenticated': False}, status=status.HTTP_401_UNAUTHORIZED) # type: ignore
