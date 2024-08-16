
from app.classes.piece import Dama, Normal
from app.classes.board import Board


class Checkers:
    def __init__(self, player1, player2):
        self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.state = "playing"
        self.player_turn = player1
        self.waiting_for = player2
        self.winner = None
        self.player1_moves = []
        self.player2_moves = []
        self.game_moves = []

    def surrender(self):
        self.state = "Finished"
        self.winner = self.waiting_for
    def make_move(self, player, start_pos, end_pos):
        if type(start_pos) != tuple and type(end_pos) != tuple:
            return "Invalid move"
        
        if player != self.player_turn:
            return f"It's {self.player_turn.name}'s turn"
        
        isValidMove, isCaptureMove = self.board.move_piece(player, start_pos, end_pos)
        
        if not isValidMove:
            return "Invalid move"
        
        if isCaptureMove:
            self.waiting_for.capture()
            self.player_turn.addCapture()
            
            if self.waiting_for.number_of_pieces == 0:
                self.state = "Finished"
                self.winner = self.player_turn
                return "Winner is " + self.player_turn.name
        
        if self.player_turn == self.player1:
            self.player1_moves.append({"start_pos": start_pos, "end_pos": end_pos})
        else:
            self.player2_moves.append({"start_pos": start_pos, "end_pos": end_pos})
        
        self.game_moves.append({"player": player.name, "start_pos": start_pos, "end_pos": end_pos})
        
        self.player_turn = self.player1 if self.player_turn == self.player2 else self.player2
        self.waiting_for = self.player2 if self.waiting_for == self.player1 else self.player1
        
        return f"Moved to {end_pos} by {player.name}"
    
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
        
    def get_state(self):
        return self.state
    
    def get_player_turn(self):
        return self.player_turn