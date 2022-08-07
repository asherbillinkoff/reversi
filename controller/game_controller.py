from model.game import Board
from model.game import Game
from model.game_logic import GameLogic
from model.human_player import HumanPlayer
from model.ai_player import AIPlayer
from view.game_view import GameView
from view.board_console_view import BoardConsoleView
from view.game_console_view import GameConsoleView

class GameController:
    '''Class is responsible for controlling all game methods in the correct order
    and passing necessary information between the view and the model (via run_game()).'''
  
    def __init__(self, view: GameView, game_model: Game) -> None:
        self.view = view
        self.model = game_model

    def start_game(self):
        board_view = BoardConsoleView(self.model.board)
        GameView = GameConsoleView(self.model, board_view)
        self.view = GameView
        
        players = []
        self.view.display_greeting_message()
        game_mode = int(self.view.get_game_mode())

        if game_mode == 1:
            human_name1 = self.view.get_human_name()
            players.append(HumanPlayer(human_name1))
            human_name2 = self.view.get_human_name()
            players.append(HumanPlayer(human_name2,symbol=2))
        elif game_mode == 2:
            human_name = self.view.get_human_name()
            players.append(HumanPlayer(human_name))
            players.append(AIPlayer())
        #elif game_mode == 3:
            # TODO - complete this section once advanced AI is built
        elif game_mode == 4:
            self.view.exit_game()

        board = Board(size=4)
        board.place_starting_pieces(players[0], players[1])
        logic = GameLogic(board, players)
        game_model = Game(board, logic, players)
        self.view.board_view = BoardConsoleView(board)
        self.model = game_model


    def run_game(self):

        while True:
            self.view.draw_board()
            score = self.model.logic.sum_player_pts(self.model.board)
            self.view.display_score(score)
            print(self.model.curr_player.name, ": it's your turn.")

            # If the current player is human, we must validate their move.
            if isinstance(self.model.curr_player, HumanPlayer):
                row, col = self.model.curr_player.get_move_human()

                # If move is invalid the player will be queried until they enter a valid one.
                self.model.logic.is_valid_move(self.model.board, row, col, self.model.curr_player, self.model.opponent)
                while not self.model.logic.is_valid:
                    print('Move is invalid')
                    row, col = self.model.curr_player.get_move_human()
                    self.model.logic.is_valid_move(self.model.board, row, col, self.model.curr_player, self.model.opponent)
                self.model.logic.make_move(self.model.board, row, col, self.model.curr_player)
            
            # For the AI turn, all provided moves are already validated by the
            # get_move_AI() method.
            elif isinstance(self.model.curr_player, AIPlayer):
                valid_moves = self.model.logic.compile_valid_moves(self.model.curr_player, self.model.opponent)
                row, col = self.model.logic.get_best_move(valid_moves, self.model.board)
                self.model.logic.make_move(self.model.board,row, col, self.model.curr_player)
            is_winner = self.model.check_winner()
            if is_winner:
                score = self.model.sum_player_pts(self.model.board)
                self.view.display_winner(is_winner)
                self.view.display_score(score)
                self.model.record_winner(score, is_winner)
                break
            self.model.change_player()