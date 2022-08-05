from view.game_view import GameView
from view.board_console_view import BoardConsoleView
from model.game import Game
from model.symbols import Symbols
# import sys

class GameConsoleView(GameView):
    '''Class is responsible for preparing necessary information for users
    to interact with the game in the console.'''
    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.board_view = BoardConsoleView(game.board)
    
    def get_opponent_type(self):
        opponent_type = input('Pick your opponent. [\'H\' for Human and \'AI\' \
for an AI bot.]')

    def get_human_name(self):
        human_name = input('Human player name: ')

    def draw_board(self):
        self.board_view.draw_board()

    def display_winner(self, player):
        self.board_view.draw_board()
        print(f'Player {Symbols(player).name} has won the game!')

    def display_score(self, score):
        print(f'Player X: {score[0]} | Player O: {score[1]}')
        print()