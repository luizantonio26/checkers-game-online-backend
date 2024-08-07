import os
from classes.piece import Dama, Normal
from colorama import Fore, Back, Style

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

    def print_board(self):
        # for row in self.board:
        #     print([piece.__str__() if piece else None for piece in row])  
        os.system('color')
        print(Style.RESET_ALL)
        print("    1    2    3    4    5    6    7    8  ")
        for i, row in enumerate(self.board): 
            line_string = f"{i+1} "
            for j, piece in enumerate(row):
                if piece:
                    if type(piece) == bool:
                        line_string += f"{Back.BLUE}     {Style.RESET_ALL}"
                    elif piece.piece_color == 'black': # type: ignore
                        if type(piece) == Dama:
                            line_string += f"{Back.BLUE}{Fore.BLACK}  \u26C3  {Style.RESET_ALL}"
                        else:
                            line_string += f"{Back.BLUE}{Fore.BLACK}  \u26C2  {Style.RESET_ALL}"
                    else:
                        if type(piece) == Dama:
                            line_string += f"{Back.BLUE}{Fore.WHITE}  \u26C1  {Style.RESET_ALL}"
                        else:
                            line_string += f"{Back.BLUE}{Fore.WHITE}  \u26C0  {Style.RESET_ALL}"
                else:
                    line_string += f"{Back.WHITE}     {Style.RESET_ALL}"
            print(line_string)
            
            