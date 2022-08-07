import sys

from model.game import Game
from model.player import Player
from view.game_view import GameView
from view.board_console_view import BoardConsoleView

class GameConsoleView(GameView):
    '''Class is responsible for preparing necessary information for users
    to interact with the game in the console.'''
    def __init__(self, game: Game, board_view: BoardConsoleView) -> None:
        super().__init__(game)
        # self.board_view = BoardConsoleView(game.board)
        self.board_view = board_view
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
        while True:
            user_mode_choice = input('Select game mode: ')
            if not(user_mode_choice.isnumeric()):
                    print('Selection invalid. Try again.')
                    continue
            elif (0 > int(user_mode_choice)) or (int(user_mode_choice) > 4):
                    print('Selection invalid. Try again.')
                    continue
            else:
                return user_mode_choice

    def get_human_name(self):
        human_name = input('Human player name: ')
        return human_name

    def draw_board(self):
        self.board_view.draw_board()

    def display_winner(self, player):
        self.board_view.draw_board()
        print(f'{player.name} has won the game!')

    def display_score(self, score, curr_player: Player, opponent: Player):
        print(f'{curr_player.name}: {score[0]} | {opponent.name}: {score[1]}')
        print()
    
    def exit_game(self):
        sys.exit('\nReversi has been exited. Thanks for playing!')
