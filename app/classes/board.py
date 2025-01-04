import os
from app.classes.piece import Dama, Normal, Piece

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

    def hasCaptureAvailable(self, piece_pos):
        piece = self.board[piece_pos[0]][piece_pos[1]]
        
        if type(piece) == bool:
            return False
        
        if piece.piece_color == 'white' and isinstance(piece, Normal):
            moves = [[-1, 1],
                     [-1, -1]
                    ]
            
            for move in moves:
                x = piece_pos[0] + move[0]
                y = piece_pos[1] + move[1]
                
                if x < 0 or x > 7 or y < 0 or y > 7:
                    continue
                
                if isinstance(self.board[x][y], Piece) and self.board[x][y].piece_color == 'black':
                    diagonal_x = x + move[0]
                    diagonal_y = y + move[1]
                    
                    if diagonal_x < 0 or diagonal_x > 7 or diagonal_y < 0 or diagonal_y > 7:
                        continue
                    
                    if type(self.board[diagonal_x][diagonal_y]) == bool:
                        return True
        elif piece.piece_color == 'black' and isinstance(piece, Normal):
            moves = [[1, 1],
                     [1, -1]
                    ]
            
            for move in moves:
                x = piece_pos[0] + move[0]
                y = piece_pos[1] + move[1]
                
                if x < 0 or x > 7 or y < 0 or y > 7:
                    continue
                
                if isinstance(self.board[x][y], Piece) and self.board[x][y].piece_color == 'white':
                    diagonal_x = x + move[0]
                    diagonal_y = y + move[1]
                    
                    if diagonal_x < 0 or diagonal_x > 7 or diagonal_y < 0 or diagonal_y > 7:
                        continue
                    
                    if type(self.board[diagonal_x][diagonal_y]) == bool:
                        return True
        else:
            moves = [[-1, 1],
                     [-1, -1],
                     [1, 1],
                     [1, -1]
                    ]
            
            for move in moves:
                x = piece_pos[0] + move[0]
                y = piece_pos[1] + move[1]
                
                if x < 0 or x > 7 or y < 0 or y > 7:
                    continue
                
                if isinstance(self.board[x][y], Piece) and self.board[x][y].piece_color != piece.piece_color:
                    diagonal_x = x + move[0]
                    diagonal_y = y + move[1]
                    
                    if diagonal_x < 0 or diagonal_x > 7 or diagonal_y < 0 or diagonal_y > 7:
                        continue
                    
                    if type(self.board[diagonal_x][diagonal_y]) == bool:
                        return True
        return False
        
        
    def move_piece(self, player, start_pos, end_pos):
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
    
    def isDama(self, pos):
        return type(self.board[pos[0]-1][pos[1]-1]) == Dama
            
            