
import redis.asyncio as redis
from redis.asyncio.lock import Lock
from app.classes.piece import Dama, Normal
from app.classes.board import Board
from app.classes.player import Player
from authentication.models import User

from gameroom.task import save_game_match, save_game_match_movement


class Checkers:
    def __init__(self, player1, player2, room_name, game_id):
        self.board = Board()
        self.player1:Player = player1
        self.player2:Player = player2
        self.status = "playing"
        self.player_turn = player1
        self.waiting_for = player2
        self.winner = None
        self.history = []
        self.room_name = room_name
        self.game_id =  game_id

    def _update_history(self, state_before_move, state_after_move, piece_type, piece_color, origin_x, origin_y, destiny_x, destiny_y, was_capture):
        self.history.append({
            "state_before_move": state_before_move,
            "state_after_move": state_after_move,
            "piece_type": piece_type,
            "piece_color": piece_color,
            "origin_x": origin_x,
            "origin_y": origin_y,
            "destiny_x": destiny_x,
            "destiny_y": destiny_y,
            "was_capture": was_capture
        })
        
    async def end_game(self):
        
        lock_key = f"lock_end_game_{self.room_name}"
        
        r = redis.Redis(host='redis', port=6379, db=0)
        
        lock = Lock(r, lock_key, timeout=20)
        if await lock.acquire():
            try:
                white_player = await User.objects.aget(nickname=self.player1.name)
                black_player = await User.objects.aget(nickname=self.player2.name)
                winner = None
                
                if self.winner:
                    winner = self.winner.name
                
                game_match = await save_game_match(white_player, black_player, self.status, winner, self.game_id)
                
                for movement in self.history:
                    move = await save_game_match_movement(game_match=game_match, **movement)
            finally:
                await lock.release()
        else:
            print("Lock já adquirido, aguardando.")
            return
        
        
        await r.close()
        
            
    
    async def surrender(self):
        if self.status == "Finished":
            return
        
        self.status = "Finished"
        self.winner = self.waiting_for
        await self.end_game()
    
    async def make_move(self, player, start_pos, end_pos):
        if type(start_pos) != tuple and type(end_pos) != tuple:
            return "Invalid move"
        
        if player != self.player_turn:
            return f"It's {self.player_turn.name}'s turn"
        
        state_before_move = self.show_state()
        isValidMove, isCaptureMove = self.board.move_piece(player, start_pos, end_pos)
        
        if not isValidMove:
            return "Invalid move"
        
        piece = self.board.board[end_pos[0]][end_pos[1]]
        piece_type = "normal" if type(piece) == Normal else "dama"
        
        if isCaptureMove:
            self.waiting_for.capture()
            self.player_turn.addCapture()
            
            if self.waiting_for.number_of_pieces == 0 and self.status != "Finished":
                self.status = "Finished"
                self.winner = self.player_turn
                await self.end_game()
                return "Winner is " + self.player_turn.name 
            
        
        # if self.player_turn == self.player1:
        #     #self.player1_moves.append({"start_pos": start_pos, "end_pos": end_pos})
            
        # else:
        #     self.player2_moves.append({"start_pos": start_pos, "end_pos": end_pos})
        
        #self.game_moves.append({"player": player.name, "start_pos": start_pos, "end_pos": end_pos})
        
        if isCaptureMove and self.board.hasCaptureAvailable(end_pos):
            return f"Piece with position {start_pos} was moved to {end_pos} by {player.name} and can capture another piece"
        
        self._update_history(
            state_before_move=state_before_move, 
            state_after_move=self.show_state(), 
            piece_type=piece_type,
            piece_color=player.piece_color,
            origin_x=start_pos[0],
            origin_y=start_pos[1],
            destiny_x=end_pos[0],
            destiny_y=end_pos[1],
            was_capture=isCaptureMove
        )
        
        self.player_turn = self.player1 if self.player_turn == self.player2 else self.player2
        self.waiting_for = self.player2 if self.waiting_for == self.player1 else self.player1
        
        return f"Piece with position {start_pos} was moved to {end_pos} by {player.name}"
            
    def isDama(self, pos):
        return self.board.isDama(pos)
    def show_state(self):
        #self.board.print_board()
        board = self.board.board
        newboard = Board(True).board
        for i, row in enumerate(board):
            for j, piece in enumerate(row):
                if piece:
                    if type(piece) == bool:
                        continue
                    elif type(piece) == Dama:
                        newboard[i][j] = { # type: ignore
                            'piece_color': piece.piece_color,
                            'piece_type': 'Dama',
                            'piece_position': piece.piece_position
                        }
                    elif type(piece) == Normal:
                        newboard[i][j] = { # type: ignore
                            'piece_color': piece.piece_color,
                            'piece_type': 'Normal',
                            'piece_position': piece.piece_position
                        }
        return newboard
        #return self.board.board
        
    def get_status(self):
        return self.status
    
    def get_player_turn(self):
        return self.player_turn