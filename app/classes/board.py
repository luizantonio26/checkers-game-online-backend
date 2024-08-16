import os
from app.classes.piece import Dama, Normal

class Board:
    def __init__(self, empty=False):
        self.board = self.initialize_valid_positions()
        self.setup_pieces(empty)
        
    def setup_pieces(self, empty=False):
        # Initialize pieces on the board
        if empty:
            return
        
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.board[row][col] = Normal('black', (row, col)) # type: ignore
                if (7 - row + col) % 2 == 1:
                    self.board[7 - row][col] = Normal('white', (7 - row, col)) # type: ignore
        
    def initialize_valid_positions(self):
        valid_positions = [[False for _ in range(8)] for _ in range(8)]
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    valid_positions[row][col] = True
        return valid_positions

    def move_piece(self, player, start_pos, end_pos):
        start_pos = (start_pos[0] - 1, start_pos[1] - 1)
        end_pos = (end_pos[0] - 1, end_pos[1] - 1)
        
        piece = self.board[start_pos[0]][start_pos[1]]
        
        
        if not piece:
            return False, False
        
        if type(piece) == bool:
            return False, False
        
        if player.piece_color != piece.piece_color:
            return False, False
        
        board, isValidMove, isCaptureMove = piece.move(end_pos, self.board)
        
        self.board = board
        
        return isValidMove, isCaptureMove
            
            