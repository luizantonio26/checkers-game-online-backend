from datetime import datetime
from celery import shared_task # type: ignore
from .models import GameMatch, GameMatchMovement

@shared_task
async def save_game_match(white_player, black_player, game_status, winner, game_id):
    game_match, created = await GameMatch.objects.aget_or_create(
        white_player=white_player, 
        black_player=black_player, 
        game_status=game_status, 
        winner=winner,
        game_id = game_id
    )
    return game_match
@shared_task
async def save_game_match_movement(game_match, state_before_move, state_after_move, piece_type, piece_color, origin_x, origin_y, destiny_x, destiny_y, was_capture):
    game_match_movement, created = await GameMatchMovement.objects.aget_or_create(
        game_match=game_match,
        piece_color=piece_color,
        piece_type=piece_type,
        origin_x=origin_x,
        origin_y=origin_y,
        destiny_x=destiny_x,
        destiny_y=destiny_y,
        state_before_move=state_before_move,
        state_after_move=state_after_move,
        was_capture=was_capture
    )
    return game_match_movement