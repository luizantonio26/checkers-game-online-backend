
from classes.board import Board


class Checkers:
    def __init__(self, player1, player2):
        self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.state = "playing"
        self.player_turn = player1
        self.waiting_for = player2
        self.winner = None

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
        
        self.player_turn = self.player1 if self.player_turn == self.player2 else self.player2
        self.waiting_for = self.player2 if self.waiting_for == self.player1 else self.player1
        
        return f"Moved to {end_pos} by {player.name}"
    
    def show_state(self):
        self.board.print_board()
        
    def get_state(self):
        return self.state
    
    def get_player_turn(self):
        return self.player_turn