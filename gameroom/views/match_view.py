from rest_framework.viewsets import GenericViewSet

from gameroom.models.game_match import GameMatch
from gameroom.serializers.match_serializer import MatchSerializer
from rest_framework.response import Response
from django.db.models import Q

class MatchViewSet(GenericViewSet):
    def list(self, request):
        if not request.user.is_authenticated:
            return Response("User is not authenticated", status=401)
        
        matches = GameMatch.objects.filter(
            Q(white_player__nickname=request.user.nickname) | Q(black_player__nickname=request.user.nickname)
        ).order_by('-match_date')
        serializer = MatchSerializer(matches, many=True)
        
        return Response(serializer.data, status=200)