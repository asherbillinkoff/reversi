from view.game_view import GameView
from model.game import Game
from model.human import Human
from model.ai_player import AIPlayer
from model.game_logic import GameLogic

class GameController:
    '''Class is responsible for controlling all game methods in the correct order
    and passing necessary information between the view and the model (via run_game()).'''
  
    def __init__(self, view: GameView, model: Game) -> None:
        self.view = view
        self.model = model

    def run_game(self):
        # TODO greeting message function in game_console_view  
        # Get the user's name and instantiate the human object.
        human_name = self.view.get_human_name()
        self.model.curr_player = Human(human_name, 1, 'White')

        # Get the opponent's type, confirm their type and instantiate the object.
        opponent = self.view.get_opponent_type()
        if opponent == 'AI':
            self.model.opponent = AIPlayer('Computer', 'Blue')
        else:
            self.model.opponent = Human('Player 2', 2, 'Blue')
        
        # Once we have the object names we can place the starting pieces on
        # the board.
        self.model.place_starting_pieces()
        while True:
            self.view.draw_board()
            score = self.model.sum_player_pts()
            self.view.display_score(score)
            print(self.model.curr_player.name, ": it's your turn.")
            row, col = self.model.curr_player.get_move()

            # If move is invalid the player will be queried until they enter a valid one.
            self.model.curr_player.game_logic.is_valid_move(row, col, self.model.curr_player.name)
            while not self.model.curr_player.game_logic.is_valid:
                print('Move is invalid')
                row, col = self.view.get_move()
                self.model.curr_player.game_logic.is_valid_move(row, col, self.model.curr_player.name)
            self.model.curr_player.game_logic.make_move(row, col)
            player = self.model.check_winner()
            if player:
                score = self.model.sum_player_pts()
                self.view.display_winner(player)
                self.view.display_score(score)
                self.model.record_winner(score, player)
                break
            self.model.change_player()