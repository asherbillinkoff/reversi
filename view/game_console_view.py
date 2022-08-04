from view.game_view import GameView
from view.board_console_view import BoardConsoleView
from model.game import Game
from model.players import Player
import sys

class GameConsoleView(GameView):
    '''Class is responsible for preparing necessary information for users
    to interact with the game in the console.'''
    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.board_view = BoardConsoleView(game.board)

    def get_move(self):
        while True:
            try:
                s = input('Enter your move (row, col):').split(',')
                if s[0] == 'e':
                    sys.exit('\nReversi has been exited. Thanks for playing!')
                row, col = int(s[0]), int(s[1])
                break
            except ValueError:
                print('Please enter an integer.')
            except IndexError:
                print('Number is out of range.')
        return row, col

    def draw_board(self):
        self.board_view.draw_board()

    def display_winner(self, player):
        self.board_view.draw_board()
        print(f'Player {Player(player).name} has won the game!')

    def display_score(self, score):
        print(f'Player X: {score[0]} | Player O: {score[1]}')
        print()