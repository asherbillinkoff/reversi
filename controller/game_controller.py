from view.game_view import GameView
from model.game import Game
# from model.new_rules import NewRules

class GameController:
  def __init__(self, view: GameView, model: Game) -> None:
    self.view = view
    self.model = model

  def run_game(self):    
    while True:
        self.view.draw_board()
        score = self.model.sum_player_pts()
        self.view.display_score(score)
        print()
        print("Player", self.model.curr_player, ": it's your turn.")
        row, col = self.view.get_move()

        # If move is invalid the player will be queried until they enter a valid one.
        self.model.is_valid_move(row, col, self.model.curr_player)
        while self.model.is_valid == False:
            print('Move is invalid')
            row, col = self.view.get_move()
            self.model.is_valid_move(row, col, self.model.curr_player)
        self.model.make_move(row, col, self.model.curr_player)
        player = self.model.check_winner()
        if player:
            self.view.display_winner(player)
            break
        self.model.change_player()