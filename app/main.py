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
        # print("Welcome to Checkers Game")
        # player1_name = input("Enter player1 name: ")
        # player1 = Player(player1_name, "white")
        
        # player2_name = input("Enter player2 name: ")
        # player2 = Player(player2_name, "black")
        
        # checkers = Checkers(player1, player2)
        
        # print("Press Enter to start the game")
        # input()

        # while checkers.get_state() == "playing":
        #     os.system("cls")
        #     print(f"{player1} {player1.captures} vs {player2.captures} {player2}")
        #     checkers.show_state()
        #     print(f"{checkers.get_player_turn().name}'s turn")
        #     piece_to_move = input(f"Select piece to move (row col) or 'ff' to surrender: ")
            
        #     if piece_to_move == "ff":
        #         checkers.surrender()
        #         break
            
        #     piece_to_move = piece_to_move.split(" ")
        #     start_pos = (int(piece_to_move[0]), int(piece_to_move[1]))
            
        #     destiny = input(f"Select destiny (row col): ")
        #     destiny = destiny.split(" ")
        #     end_pos = (int(destiny[0]), int(destiny[1]))
            
        #     game_log = checkers.make_move(checkers.get_player_turn(), start_pos=start_pos, end_pos=end_pos)
        #     print(game_log)
            
        #     input("Press Enter to continue...")

        # print(f"Winner is {checkers.winner.name}") # type: ignore
        
        board = Board(empty=True)
        
        player1 = Player("player1_name", "white")
        player2 = Player("player2_name", "black")
        
        board.board[3][2] = Normal("black", (3, 2))
        board.board[4][3] = Normal("white", (4, 3))
        
        board.print_board()
        
        board.move_piece(player2, (4, 3), (6, 5))
        
        board.print_board()
        
if __name__ == "__main__":
    main = Main()
    main.main()