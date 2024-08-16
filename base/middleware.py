
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken
from django.contrib.auth import get_user_model
from jwt import decode as jwt_decode
from jwt.exceptions import InvalidTokenError
from django.conf import settings

User = get_user_model()

@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            token_name, token_key = headers[b'authorization'].decode().split()
            try:
                UntypedToken(token_key)
                decoded_data = jwt_decode(token_key, settings.SECRET_KEY, algorithms=["HS256"])
                user = await get_user(decoded_data['user_id'])
                scope['user'] = user
            except InvalidTokenError:
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()
        return await super().__call__(scope, receive, send)