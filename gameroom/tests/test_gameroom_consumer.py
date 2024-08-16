import time
import pytest
from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase
from gameroom.consumers.gameroom_consumer import GameRoomConsumer
from base.asgi import application
from authentication.models.user import User

@pytest.mark.asyncio
class TestGameRoomConsumer(TransactionTestCase):
    def setUp(self):
        user1 = User.objects.create_user(
            email="WqKQ7@example.com",
            nickname="tonho",
            first_name="test",
            last_name="test",
            password="test123"
        )
        
        self.user1 = user1
        self.token1 = user1.get_tokens()['access']
        
        user2 = User.objects.create_user(
            email="WqKQ73@example.com",
            nickname="luiz",
            first_name="test",
            last_name="test",
            password="test123"
        )
        
        self.user2 = user2
        self.token2 = user2.get_tokens()['access']
        
    async def test_websocket_communication(self):
        # Configurando o WebsocketCommunicator        
        communicator = WebsocketCommunicator(application, "gameroom/teste/", headers=[
                (b"authorization", f"Bearer {self.token1}".encode("utf-8"))
            ])
        
        connected, subprotocol = await communicator.connect()
        assert connected
        response = await communicator.receive_json_from()

        # Enviando uma mensagem pelo WebSocket
        await communicator.send_json_to({
            "action": "chat_message",
            "message": "hello"
        })

        # Verificando se a resposta é a esperada
        response = await communicator.receive_json_from()
        assert response == {"message": "hello", "username": self.user1.nickname}

        # Fechando o WebSocket
        await communicator.disconnect()
        
    async def test_start_game(self):
        # Configurando o WebsocketCommunicator        
        tonho = WebsocketCommunicator(application, "gameroom/teste/", headers=[
                (b"authorization", f"Bearer {self.token1}".encode("utf-8"))
            ])
        
        connected_tonho, _ = await tonho.connect()
        assert connected_tonho
        response = await tonho.receive_json_from()
        
        luiz = WebsocketCommunicator(application, "gameroom/teste/", headers=[
                (b"authorization", f"Bearer {self.token2}".encode("utf-8"))
            ])
        
        connected_luiz, _ = await luiz.connect()
        assert connected_luiz
        response = await luiz.receive_json_from()
        response = await tonho.receive_json_from()
        # Enviando uma mensagem pelo WebSocket
        await tonho.send_json_to({
            "action": "game_start"
        })

        # Verificando se a resposta é a esperada
        response_tonho = await tonho.receive_json_from()
        response_luiz = await luiz.receive_json_from()
        #print(response_tonho, response_luiz)
        
        self.assertEqual(response_tonho, response_luiz)
        self.assertEqual(response_tonho["game_has_started"], True)
        self.assertEqual(response_tonho["player1"], self.user1.nickname)
        self.assertEqual(response_tonho["player2"], self.user2.nickname)
        
        # Fechando o WebSocket
        await tonho.disconnect()
        await luiz.disconnect()