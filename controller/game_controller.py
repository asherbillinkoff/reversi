from model.game import Board
from model.game import Game
from model.game_logic import GameLogic
from model.human_player import HumanPlayer
from model.ai_player import AIPlayer
from view.game_view import GameView
from view.board_console_view import BoardConsoleView
from view.game_console_view import GameConsoleView

class GameController:
    """    Class is responsible for controlling all game methods in the correct order
    and passing necessary information between the view and the model (via run_game()).
    """
  
    def __init__(self, view: GameView, game_model: Game) -> None:
        self.view = view
        self.model = game_model

    def start_game(self):
        """    Initializes the game with information like player names, game mode,
        and all of the game objects.
        """

        board_view = BoardConsoleView(self.model.board)
        self.view = GameConsoleView(self.model, board_view)
        
        self.players = []
        self.view.display_greeting_message()
        game_mode = int(self.view.get_game_mode())
        if game_mode == 1:
            human_name1 = self.view.get_human_name()
            self.players.append(HumanPlayer(human_name1))
            human_name2 = self.view.get_human_name()
            self.players.append(HumanPlayer(human_name2,symbol=2))
        elif game_mode == 2:
            human_name = self.view.get_human_name()
            self.players.append(HumanPlayer(human_name))
            self.depth = self.view.get_ai_depth()
            self.players.append(AIPlayer(depth=self.depth))
        elif game_mode == 3:
            self.view.exit_game()

        board = Board(size=4)
        board.place_starting_pieces(self.players[0], self.players[1])
        logic = GameLogic()
        game_model = Game(board, logic, self.players)
        self.view.board_view = BoardConsoleView(board)
        self.model = game_model


    def run_game(self):
        """    Main function of the game which controls all of the in-game operations
        including currents turns, displaying board status, getting moves, validating
        moves, making moves, checking for a winner and more.
        """

        # Counter keeps track of instances when a player has no more valid moves.
        # If both players are at a stalemate the game ends (is_over_counter > 1)
        skipped_turns = 0
        while True:

            self.view.draw_board()
            score = self.model.logic.sum_player_pts(self.model.board)
            self.view.display_score(score, self.players)
            print(self.model.curr_player.name, ": it's your turn.")

            # If the current player is human, move must be validated.
            if isinstance(self.model.curr_player, HumanPlayer):
                row, col = self.model.curr_player.get_move_human()

                # If move is invalid the player will be queried until they enter a valid one.
                self.model.logic.is_valid_move(self.model.board, row, col, self.model.curr_player, self.model.opponent)
                directions = self.model.logic.is_valid_move(self.model.board, row, col, self.model.curr_player, self.model.opponent)
                
                # If there are no valid moves on the board, increment the counter.
                if directions is None:
                    skipped_turns += 1
                else:
                    while not self.model.logic.is_valid:
                        print('Move is invalid')
                        row, col = self.model.curr_player.get_move_human()
                        directions = self.model.logic.is_valid_move(self.model.board, row, col, self.model.curr_player, self.model.opponent)
                    self.model.logic.make_move(self.model.board, row, col, directions, self.model.curr_player)
            
            # For the AI turn all moves have already been validated.
            elif isinstance(self.model.curr_player, AIPlayer):
                #valid_moves = self.model.logic.compile_valid_moves(self.model.curr_player, self.model.opponent)
                row, col = self.model.logic.choose_move(self.model.board, self.model.curr_player.depth, self.model.curr_player, self.model.opponent)
                
                # If there are no valid moves on the board, increment the counter.
                if row is None:
                    skipped_turns += 1
                else:
                    directions = self.model.logic.is_valid_move(self.model.board, row, col, self.model.curr_player, self.model.opponent)
                    self.model.logic.make_move(self.model.board,row, col, directions, self.model.curr_player)

            # If there have been more than 2 skipped turns OR the board is full
            # then check_winner will return a player object and enter into the
            #final loop of the game.
            is_winner = self.model.check_winner(skipped_turns)
            if is_winner:
                score = self.model.logic.sum_player_pts(self.model.board)
                self.view.display_winner(is_winner)
                self.view.display_score(score, self.players)
                self.model.record_winner(score, is_winner)
                break
            self.model.change_player()