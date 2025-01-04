from rest_framework import serializers
from gameroom.models import GameMatch
from gameroom.models.game_match import GameMatchMovement
from gameroom.serializers.match_moviments_serializer import MatchMovimentsSerializer

class MatchSerializer(serializers.ModelSerializer):
    game_id = serializers.UUIDField(read_only=True)
    match_date = serializers.DateTimeField(read_only=True)
    white_player = serializers.CharField(read_only=True, source='white_player.nickname')
    black_player = serializers.CharField(read_only=True, source='black_player.nickname')
    winner = serializers.CharField(read_only=True)
    game_status = serializers.CharField(read_only=True)
    movements = MatchMovimentsSerializer(source='gamematchmovement_set', many=True, read_only=True)
    
    class Meta:
        
        model = GameMatch
        fields = ['game_id', 'match_date', 'white_player', 'black_player', 'winner', 'game_status', 'movements']