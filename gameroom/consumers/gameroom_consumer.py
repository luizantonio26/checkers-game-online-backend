from email import message
import json
from time import sleep

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
from app.classes.piece import Dama
from app.classes.player import Player
import uuid

class GameRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #print("opa")
        if self.scope['user'].is_anonymous:
            raise DenyConnection("User is not authenticated")
        
        self.room_name = self.scope['url_route']['kwargs'].get('room_name')
        if not self.room_name:
            raise DenyConnection("Invalid room name")
        
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
        
        self.connected_users = connected_users
        
        if len(connected_users) == 1:
            self.player = Player(self.scope['user'].nickname, "white")
            self.host = self.scope['user'].nickname
            
        else:
            self.player = Player(self.scope['user'].nickname, "black")
            self.host = connected_users[0]
        
        await self.accept()
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'join',
                'data': {'username':self.scope['user'].nickname}
            }
        )
    
    
    async def disconnect(self, close_code):
        # Verifica se room_name foi definido
        if hasattr(self, 'room_name'):
            await self.remove_user_from_room(self.room_name, self.username)
            try:
                if self.game:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'surrender',
                        }
                    )
            except AttributeError:
                pass    
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'leave',
                    'data': {'username': self.username},
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
        
        if action == 'ready':
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'ready',
                'player': self.scope['user'].nickname
            })
        
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
            
            self.game_id = uuid.uuid4()
            # Envie a mensagem para todos no grupo, incluindo informações sobre os jogadores
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_start',
                    'player1': player1,
                    'player2': player2,
                    'game_id': str(self.game_id)
                }
            )
        
        if action == 'show_players':
            # await self.send(text_data=json.dumps({
            #     "players": connected_users
            # }))
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'show_players',
                'players': connected_users,
                'host': self.host
            })
        
        elif action == 'show_state':
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'show_state'
            }
        )
            
        elif action == 'make_move':
            player = self.player.name
            start_pos = (text_data_json['data']['start_pos'][0], text_data_json['data']['start_pos'][1])
            end_pos = (text_data_json['data']['end_pos'][0], text_data_json['data']['end_pos'][1])
            
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
                    'message': text_data_json['data']['message'],
                    'username': self.scope['user'].nickname,
                }
            )
        
        elif action == 'surrender':
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'surrender'
            })
    
    async def ready(self, event):
        await self.send(text_data=json.dumps({
            "type": "ready",
            "data": {"player":event["player"]}
        }))
    
    async def surrender(self, event):
        await self.game.surrender()
        await self.send(text_data=json.dumps({
            "type": "surrender",
            "data": {"winner":self.game.winner.name} # type: ignore
        }))    

    async def show_players(self, event):
        await self.send(text_data=json.dumps({
            "type": "show_players",
            "data": {"players": event["players"], 
                     "host": event["host"]
                    }
        }))
    
    async def game_start(self, event):
        self.player1 = Player(event['player1'], 'white')
        self.player2 = Player(event['player2'], 'black')
        self.game_id = event['game_id']
        
        self.game = Checkers(
            player1=self.player1,
            player2=self.player2,
            room_name=self.room_name,
            game_id = self.game_id
        )
        
        await self.send(text_data=json.dumps({
            "type": "game_start",
            "data": {
                "game_has_started": True,
                "game_state": self.game.show_state(),
                'player1': self.player1.name,
                'player2': self.player2.name,
                'current_player': self.game.player_turn.name,
                'game_id': self.game_id
            }
        }))
        
    async def make_move(self, event):
        player = self.player1 if event['player'] == self.player1.name else self.player2
        start_pos = event['start_pos']
        end_pos = event['end_pos']
        
        move_info = await self.game.make_move(player, (start_pos[0], start_pos[1]), (end_pos[0], end_pos[1]))
        isDama = self.game.isDama((end_pos[0], end_pos[1]))
        await self.send(text_data=json.dumps({
            "type": "make_move",
            "data": {
                "move_info": move_info,
                "turned_dama": isDama,
                "game_state": self.game.show_state(),
                "game_status": self.game.get_status(),
                "current_player": self.game.player_turn.name,
                "next_player": self.game.waiting_for.name,
                "piece_moved": end_pos
            }
        }))
        
    async def show_state(self, event):
        state = self.game.show_state()
        await self.send(text_data=json.dumps({
            "type": "show_state",
            "data": {"state":state}
        }))
    
    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'data': {
            'message': message,
            'username': event['username'],
            }
        }))
        
    async def join(self, event):
        await self.send(text_data=json.dumps({
            'type': 'join',
            'data':{'nickname': event['data']['username']},
        }))
    
    async def leave(self, event):
        await self.send(text_data=json.dumps({
            'type': 'leave',
            'data':{'nickname': event['data']['username']},
        }))
    @staticmethod
    async def get_uuid(room_name):
        channel_layer = get_channel_layer()
        # Assuming Redis is used, use group_channels to get all users in the room
        room_id = await channel_layer.get_group_channels(f'room_id_{room_name}')
        
        return room_id
    @staticmethod
    async def add_user_to_room(room_name, user):
        channel_layer = get_channel_layer()
        
        user = user.replace(' ', '')
                
        await channel_layer.group_add(f'users_{room_name}', user)
        # Keep track of the user names in the room
        room_users = await channel_layer.get_group_channels(f'users_{room_name}')
        
        return room_users

    @staticmethod
    async def get_connected_users(room_name):
        channel_layer = get_channel_layer()
        # Assuming Redis is used, use group_channels to get all users in the room
        room_users = await channel_layer.get_group_channels(f'users_{room_name}')
        
        return room_users

    @staticmethod
    async def remove_user_from_room(room_name, user):
        channel_layer = get_channel_layer()
        user = user.replace(' ', '')
        await channel_layer.group_discard(f'users_{room_name}', user)

