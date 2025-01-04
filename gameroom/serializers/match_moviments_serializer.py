from rest_framework import serializers
from gameroom.models import GameMatchMovement

class MatchMovimentsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    piece_color = serializers.CharField(read_only=True)
    piece_type = serializers.CharField(read_only=True)
    state_before_move = serializers.JSONField(read_only=True)
    state_after_move = serializers.JSONField(read_only=True)
    was_capture = serializers.BooleanField(read_only=True)
    origin_x = serializers.IntegerField(read_only=True)
    origin_y = serializers.IntegerField(read_only=True)
    destiny_x = serializers.IntegerField(read_only=True)
    destiny_y = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = GameMatchMovement
        fields = [
                'id',
                    'piece_color', 
                  'piece_type', 
                  'state_before_move',
                  'state_after_move', 
                  'was_capture', 
                  'origin_x', 
                  'origin_y', 
                  'destiny_x', 
                  'destiny_y']