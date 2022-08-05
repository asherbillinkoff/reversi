from model.game import Game
from model.game_logic import GameLogic
from model.player import Player
from copy import deepcopy

class AIPlayer(Player):
    def __init__(self, name, colour):
        super().__init__(name, colour)
        self.game = Game()
        self.game_logic = GameLogic()
        self.name = name
        self.symbol = 3

    def compile_next_moves(self, board):
        valid_moves = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    if self.game_logic.is_valid_move(i, j, self.name):
                        valid_moves.append((i,j))
        return valid_moves

    def calculate_move_scores(self, valid_moves, board):
        test_board = deepcopy(board)
        for move in valid_moves:
            test_board[move[0]][move[1]] = self.name
            score = self.game.sum_player_pts()
            difference = score[0] - score[1]
            valid_moves[move] = (move[0], move[1], difference)
        return max(valid_moves, key=lambda x:x[2])

    def get_move_AI(self, board):
        valid_moves = AIPlayer.compile_next_moves(self, board)
        move = AIPlayer.calculate_move_scores(self, valid_moves, board)
        return move[0], move[1]
