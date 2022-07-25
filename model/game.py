from abc import ABC, abstractmethod
from players import Player
from model.board import Board

class Game(ABC):
    def __init__(self, board_size):
        super().__init__(self)
        self.board = Board(board_size)
        self.curr_player = Player.X

    def change_player(self):
        curr_player = 3 - curr_player

    def make_move(self):
        self.board.update_cell(row, col, self.curr_player)

    def sum_player_pts(self):
        sum_X = 0
        sum_O = 0
        for i in range(board_size):
            for j in range(board_size):
                if self.board.mat[i][j] == 1:
                    sum_X += 1
                elif self.mat[i][j] == 2:
                    sum_O += 1
        return (sum_X, sum_O)


    def check_winner(self):
        for i in range(board_size):
            for j in range(board_size):
                if self.board.mat[i][j] == 0:
                    return 

    @abstractmethod
    def is_valid_move(self, row, col):
        pass
    