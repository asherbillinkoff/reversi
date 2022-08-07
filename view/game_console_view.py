import sys

from view.game_view import GameView
from view.board_console_view import BoardConsoleView
from model.game import Game

class GameConsoleView(GameView):
    '''Class is responsible for preparing necessary information for users
    to interact with the game in the console.'''
    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.board_view = BoardConsoleView(game.board)
        self.game = game
    
    def display_greeting_message(self):
        print('''
        =================================
        X                               O
        X                               O
        X           REVERSI             O
        X                               O
        X                               O
        =================================

        Welcome to Reversi.

        The game mode options are:

        1. Human vs. Human.
        2. Human vs. Simple AI
        3. Human vs Advanced AI
        4. Exit the game.
        '''
        )

    def get_game_mode(self):
        user_mode_choice = input('Select game mode: ')
        if not int(user_mode_choice) and (user_mode_choice not in range(1,5)):
            print('Selection invalid. Try again.')
            self.get_game_mode(self)
        return user_mode_choice

    def get_human_name(self):
        human_name = input('Human player name: ')
        return human_name

    def draw_board(self):
        self.board_view.draw_board()

    def display_winner(self, player):
        self.board_view.draw_board()
        print(f'{player.name} has won the game!')

    def display_score(self, score):
        print(f'{self.game.player1.name}: {score[0]} | {self.game.player2.name}: {score[1]}')
        print()
    
    def exit_game(self):
        sys.exit('\nReversi has been exited. Thanks for playing!')
