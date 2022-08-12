import unittest
from model.human_player import HumanPlayer
from model.game_logic import GameLogic
from model.game import Game

player1 = HumanPlayer('Alice')
player2 = HumanPlayer('Bob')
players = [player1, player2]
game_logic = GameLogic()

# For validating logic at the beginning of the game.
start_board = [[0,0,0,0]
                [0,1,2,0]
                [0,2,1,0]
                [0,0,0,0]]

# start_game = Game(start_board, game_logic, players)

# For validating logic near the end of the game.
ending_board = [[0,1,1,2],
            [1,1,1,1],
            [1,1,1,1],
            [1,1,1,2]]

# For validating logic on the completed board.
complete_board = [[2,2,2,2],
            [1,2,1,1],
            [1,1,2,1],
            [1,1,1,2]]

complete_game = Game(complete_board,game_logic, players)

# Expected result from is_valid_move on an opening move of (2,0) by player 1.
# The result1 is the valid direction in which the move will execute on the board.
result1 = [(0,1)]

# Expected result when is_valid_move cannot find any valid moves on the board for
# a given user move.
result2 = None

# Expected result when player 2 fills the last empty cell on the board.
# The result3 is the valid direction in which the move will execute on the board.
result3 = [(0,1),(1,1)]

class TestGameLogic(unittest.TestCase):
    def test_is_valid_moves(self):
        # Valid move should return a list of valid directions.
        self.assertEqual(game_logic.is_valid_move(start_board, 2, 0, player1, player2), result1)

        # Score before the first move should be Alice (2): Bob (2).
        self.assertEqual(game_logic.sum_player_pts(start_board), (2,2))

        # Invalid move on an empty cell should return an empty list.
        self.assertEqual(game_logic.is_valid_move(start_board, 1, 0, player1, player2), result2)

        # Invalid move on an occupied cell should return an empty list.
        self.assertEqual(game_logic.is_valid_move(start_board, 1, 0, player1, player2), result2)

        # Valid move on the last empty cell should return a list with two valid directions.
        self.assertEqual(game_logic.is_valid_move(ending_board, 0, 0, player2, player1), result3)

        # Final score should be Alice (2): Bob (2).
        self.assertEqual(game_logic.sum_player_pts(complete_board), (9,7))

        # Check winner should return player 1 (Alice).
        self.assertEqual(complete_game.check_winner(0), player1)


