import os
from classes.board import Board
from classes.checkers import Checkers
from classes.piece import Normal
from classes.player import Player

class Main(object):
    def __init__(self):
        pass
    
    def main(self):
        os.system("cls")
        checkers = Checkers(Player("player1", "white"), Player("player2", "black"))
        
        print(checkers.show_state())
        
if __name__ == "__main__":
    main = Main()
    main.main()