from django.urls import path

from base.consumer import TestConsumer
from gameroom.consumers.gameroom_consumer import GameRoomConsumer

websocket_urlpatterns = [
    path("gameroom/<str:room_name>/", GameRoomConsumer.as_asgi()),
    path("ws/test/", TestConsumer.as_asgi()),
]
