class Player:

    def __init__(self, name, piece_color):
        self.name = name
        self.piece_color = piece_color
        self.captures = 0
        self.number_of_pieces = 12
    
    def addCapture(self):
        self.captures += 1
    
    def capture(self):
        self.number_of_pieces -= 1
    
    def __str__(self):
        return self.name