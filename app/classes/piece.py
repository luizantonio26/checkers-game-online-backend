from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self, type_of_movements, num_of_movements, rule_for_kill, piece_color, piece_position):
        self.type_of_movements = type_of_movements
        self.num_of_movements = num_of_movements
        self.rule_for_kill = rule_for_kill,
        self.piece_color = piece_color
        self.piece_position = piece_position
        
    @abstractmethod
    def move(self, end_pos):
        pass

    @abstractmethod
    def can_move(self, end_pos, board):
        pass
    
    def __str__(self):
        return self.piece_color
    
class Normal(Piece):
    def __init__(self, piece_color, piece_position):
        super().__init__('diagonal', 1, 'simple', piece_color, piece_position)

    def move(self, end_pos, board):
        start_pos = self.piece_position
        row_diff = self.piece_position[0] - end_pos[0]
        becameDama = False
        
        if not self.can_move(end_pos, board):
            return board, False, False
    
        self.piece_position = end_pos
        
        if self.piece_color == "white" and start_pos[0] == 1:
            board[end_pos[0]][end_pos[1]] = Dama(self.piece_color, self.piece_position)
        elif self.piece_color == "black" and start_pos[0] == 6:
            board[end_pos[0]][end_pos[1]] = Dama(self.piece_color, self.piece_position)
        else:
            board[end_pos[0]][end_pos[1]] = self
            
        board[start_pos[0]][start_pos[1]] = True
    
        # Implement move logic for Normal piece
        isCaptureMove = False
        if abs(row_diff) > 1:
            isCaptureMove = True
            if self.piece_color == 'black':
                if start_pos[1] > end_pos[1]:
                    board[start_pos[0]+1][start_pos[1]-1] = True
                else:
                    board[start_pos[0]+1][start_pos[1]+1] = True
            else:
                if start_pos[1] < end_pos[1]:
                    board[start_pos[0]-1][start_pos[1]+1] = True
                else:
                    board[start_pos[0]-1][start_pos[1]-1] = True
        
        return board, True, isCaptureMove
        

    def can_move(self, end_pos, board):
        start_pos = self.piece_position
        
        if self.piece_color == 'black' and end_pos[0] < start_pos[0]:
            return False

        if self.piece_color == 'white' and end_pos[0] > start_pos[0]:
            return False
        
        # Implement movement validation for Normal piece
        row_diff = abs(end_pos[0] - start_pos[0])
        col_diff = abs(end_pos[1] - start_pos[1])

        # Verifique se o movimento é diagonal
        if row_diff != col_diff:
            return False
        
        if start_pos[0] == end_pos[0] or start_pos[1] == end_pos[1]:
            return False 
        
        if not board[end_pos[0]][end_pos[1]]:
            return False

        if isinstance(board[end_pos[0]][end_pos[1]], Piece):
            return False
        
        row_step = 1 if end_pos[0] > start_pos[0] else -1
        col_step = 1 if end_pos[1] > start_pos[1] else -1

        if row_diff > 2:
            return False
        
        if row_diff == 2:
            if self.piece_color == 'black':
                if start_pos[1] > end_pos[1]:
                    middle_piece = board[start_pos[0]+1][start_pos[1]-1]
                else:
                    middle_piece = board[start_pos[0]+1][start_pos[1]+1]
            else:
                if start_pos[1] < end_pos[1]:
                    middle_piece = board[start_pos[0]-1][start_pos[1]+1]
                else:
                    middle_piece = board[start_pos[0]-1][start_pos[1]-1]
                
            if not isinstance(middle_piece, Piece):
                return False
            
            if middle_piece.piece_color == self.piece_color:
                return False
    
        # Verifique se todas as posições no caminho estão livres
        # for i in range(1, row_diff):
        #     if isinstance(board[start_pos[0] + i * row_step][start_pos[1] + i * col_step], Piece):
        #         return False
        
        return True
    def __str__(self):
        return self.piece_color

class Dama(Piece):
    def __init__(self, piece_color, piece_position):
        super().__init__('diagonal', float('inf'), 'jump', piece_color, piece_position)

    def move(self, end_pos, board):
        # Implement move logic for Dama piece
        start_pos = self.piece_position
        row_diff = end_pos[0] - start_pos[0]
        if not self.can_move(end_pos, board):
            return board, False, False
    
        self.piece_position = end_pos
        board[end_pos[0]][end_pos[1]] = self
        board[start_pos[0]][start_pos[1]] = True
    
        # Implement move logic for Normal piece
        isCaptureMove = False
        if abs(row_diff) == 2:
            isCaptureMove = True
            if row_diff > 0:
                if start_pos[1] > end_pos[1]:
                    board[start_pos[0]+1][start_pos[1]-1] = True
                else:
                    board[start_pos[0]+1][start_pos[1]+1] = True
            else:
                if start_pos[1] < end_pos[1]:
                    board[start_pos[0]-1][start_pos[1]+1] = True
                else:
                    board[start_pos[0]-1][start_pos[1]-1] = True
        
        return board, True, isCaptureMove

    def can_move(self, end_pos, board):
        start_pos = self.piece_position
        
        # Implement movement validation for Normal piece
        row_diff = end_pos[0] - start_pos[0]
        col_diff = abs(end_pos[1] - start_pos[1])

        # Verifique se o movimento é diagonal
        if abs(row_diff) != col_diff:
            return False
        
        if start_pos[0] == end_pos[0] or start_pos[1] == end_pos[1]:
            return False 
        
        if not board[end_pos[0]][end_pos[1]]:
            return False

        if isinstance(board[end_pos[0]][end_pos[1]], Piece):
            return False
        
        row_step = 1 if end_pos[0] > start_pos[0] else -1
        col_step = 1 if end_pos[1] > start_pos[1] else -1

        if abs(row_diff) > 2:
            return False
        
        if abs(row_diff) == 2:
            if row_diff > 0:
                if start_pos[1] > end_pos[1]:
                    middle_piece = board[start_pos[0]+1][start_pos[1]-1]
                else:
                    middle_piece = board[start_pos[0]+1][start_pos[1]+1]
            else:
                if start_pos[1] < end_pos[1]:
                    middle_piece = board[start_pos[0]-1][start_pos[1]+1]
                else:
                    middle_piece = board[start_pos[0]-1][start_pos[1]-1]
                
            if not isinstance(middle_piece, Piece):
                return False
            
            if middle_piece.piece_color == self.piece_color:
                return False
            
        # Verifique se todas as posições no caminho estão livres
        # for i in range(1, row_diff):
        #     if isinstance(board[start_pos[0] + i * row_step][start_pos[1] + i * col_step], Piece):
        #         return False
        
        return True
    
    def __str__(self):
        return self.piece_color