from email import message
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils import timezone
from django.utils.timezone import make_aware
from channels.exceptions import DenyConnection
from channels.layers import get_channel_layer
from channels_redis.core import RedisChannelLayer

from app.classes.checkers import Checkers
from app.classes.player import Player

class GameRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_anonymous:
            raise DenyConnection("User is not authenticated")
        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'gameroom_%s' % self.room_name
        self.username = self.scope['user'].nickname
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        connected_users = await self.add_user_to_room(self.room_name, self.scope['user'].nickname)
        
        if not connected_users or len(connected_users) > 2:
            raise DenyConnection("Room is full")
        
        if len(connected_users) == 1:
            self.player = Player(self.scope['user'].nickname, "white")
        else:
            self.player = Player(self.scope['user'].nickname, "black")
        
        await self.accept()
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'join',
                'username': self.scope['user'].nickname
            }
        )
    
    
    async def disconnect(self, close_code):
        await self.remove_user_from_room(self.room_name, self.scope['user'].nickname)
        
        if self.scope['user'].is_anonymous:
            return
        # Sair do grupo da sala ao desconectar
        
        self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'leave',
                'username': self.scope['user'].nickname
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']

        connected_users = await self.get_connected_users(self.room_name)
        
        if action == 'game_start':
            # Determinar os jogadores com base nas cores
            player1 = self.player.name if self.player.piece_color == "white" else Player(
                name=connected_users[0] if connected_users[0] != self.player.name else connected_users[1],
                piece_color="white"
            ).name
            player2 = self.player.name if self.player.piece_color == "black" else Player(
                name=connected_users[0] if connected_users[0] != self.player.name else connected_users[1],
                piece_color="black"
            ).name
            
            # Envie a mensagem para todos no grupo, incluindo informações sobre os jogadores
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_start',
                    'player1': player1,
                    'player2': player2
                }
            )
        
        if action == 'show_players':
            await self.send(text_data=json.dumps({
                "players": f"Player 1 - {self.player1.name} {self.player1.piece_color}  vs Player 2 -{self.player2.name} {self.player2.piece_color}"
            }))
        
        elif action == 'show_state':
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'show_state',
                'state': self.game.show_state(),
            }
        )
            
        elif action == 'make_move':
            player = self.player.name
            start_pos = (text_data_json['start_pos'][0], text_data_json['start_pos'][1])
            end_pos = (text_data_json['end_pos'][0], text_data_json['end_pos'][1])
            
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'make_move',
                'player': player,
                'start_pos': start_pos,
                'end_pos': end_pos
            })
            
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'show_state',
                'state': self.game.show_state(),
            })
            
        elif action == 'chat_message':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': text_data_json['message'],
                    'username': self.scope['user'].nickname,
                }
            )
    
    async def show_players(self, event):
        await self.send(text_data=json.dumps({
            "players": event["players"]
        }))
    async def game_start(self, event):
        self.player1 = Player(event['player1'], 'white')
        self.player2 = Player(event['player2'], 'black')
        
        self.game = Checkers(
            player1=self.player1,
            player2=self.player2,
        )
        
        await self.send(text_data=json.dumps({
            "game_has_started": True,
            "game_state": self.game.show_state(),
            'player1': self.player1.name,
            'player2': self.player2.name
        }))
        
    async def make_move(self, event):
        player = self.player1 if event['player'] == self.player1.name else self.player2
        start_pos = event['start_pos']
        end_pos = event['end_pos']
        
        current_player = self.game.player_turn.name
        next_player = self.game.waiting_for.name
        move_info = self.game.make_move(player, (start_pos[0], start_pos[1]), (end_pos[0], end_pos[1]))
        await self.send(text_data=json.dumps({
            "move_info": move_info,
            "current_player": current_player,
            "next_player": next_player
        }))
    async def show_state(self, event):
        state = event["state"]
        
        await self.send(text_data=json.dumps({
            "state":state
        }))
    
    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': event['username'],
        }))
        
    async def join(self, event):
        await self.send(text_data=json.dumps({
            'type': 'join',
            'message': event['username'] + ' joined the room',
        }))
    
    async def leave(self, event):
        await self.send(text_data=json.dumps({
            'type': 'leave',
            'message': event['username'] + ' left the room',
        }))
        
        
    @staticmethod
    async def add_user_to_room(room_name, user):
        channel_layer = get_channel_layer()
                    
        await channel_layer.group_add(f'users_{room_name}', user)
        # Keep track of the user names in the room
        room_users = await channel_layer.get_group_channels(f'users_{room_name}')
        
        # if room_name not in room_users:
        #     room_users[room_name] = []
        # room_users[room_name].append(username)
        return room_users#[room_name]

    @staticmethod
    async def get_connected_users(room_name):
        channel_layer = get_channel_layer()
        # Assuming Redis is used, use group_channels to get all users in the room
        room_users = await channel_layer.get_group_channels(f'users_{room_name}')
        
        return room_users

    @staticmethod
    async def remove_user_from_room(room_name, user):
        channel_layer = get_channel_layer()
        await channel_layer.group_discard(f'users_{room_name}', user)

    