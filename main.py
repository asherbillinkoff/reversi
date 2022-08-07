from model.game import Game
from model.board import Board
from model.game_logic import GameLogic
from model.human_player import HumanPlayer
from view.game_console_view import GameConsoleView
from controller.game_controller import GameController


players = [HumanPlayer('P1', 0), HumanPlayer('P2', 0)]
board = Board()
logic = GameLogic(board, players)
model = Game(board, logic, players)
view = GameConsoleView(model)
controller = GameController(view, model)

controller.start_game()
controller.run_game()
