from model.board import Board
from model.player import Player

from copy import deepcopy


class GameLogic:
    def __init__(self, board: Board, players):
        self.board = board
        self.is_valid = False
        self.curr_player = players[0]
        self.opponent = players[1]
        self.valid_moves = []

    def make_move(self, board: Board, row, col, player: Player):
        """ Method pass along a user move to the board to be updated."""

        symbol = player.symbol
        self.board.update_cell(row, col, symbol)

    def is_valid_move(self, board: Board, row, col, player: Player, opponent: Player):
        ''' Function determines if the user move is valid. If the
        three condition checks pass then the recursive function is called to
        flip opponent disks.'''

        # Create a list of all directions in which a valid move exists.
        true_directions = []
        self.is_valid = False
        
        # Valid move condition #1: the cell is empty.
        if self.board.get_cell(row, col) == 0:
            directions = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
            cell = (row, col)
            for direction in directions:
                check_cell = (row + direction[0], col + direction[1])

                # Check to make sure the index is in range of our board.
                if max(check_cell) >= self.board.size or min(check_cell) < 0:
                    continue

                # Valid move condition #2: there is an adjacent cell with the
                # other player's disk.
                if self.board.mat[check_cell[0]][check_cell[1]] == opponent.symbol:

                    # Increment the current cell in that direction.
                    cell = (cell[0] + direction[0], cell[1] + direction[1])
                    if max(cell) >= self.board.size or min(cell) < 0:
                        continue

                    # Valid move condition #3: the given direction contains
                    # another one of current player's disks further down the
                    # row (i.e. there is a valid disk sandwich).
                    next_cell = cell
                    while self.board.mat[next_cell[0]][next_cell[1]] == opponent.symbol:
                        next_cell = (next_cell[0] + direction[0],
                                    next_cell[1] + direction[1])
                        # Make sure that the incremented cell is still within
                        # board range.
                        if max(next_cell) >= self.board.size or min(next_cell) < 0:
                            self.is_valid = False
                            break
                        # If incremented cell is = player then move is valid.
                        elif self.board.mat[next_cell[0]][next_cell[1]] == player.symbol:
                            self.is_valid = True
                            break
                            
                    # When code reaches the end of the disk sandwich, it
                    # appends that direction to a list
                    if self.is_valid:
                        true_directions.append(direction)    
                cell = (row, col)
                self.is_valid = False
        else:
            return

        # Need to confirm if any valid directions exist for placing a disk    
        if true_directions != []:
            self.board.update_board(row, col, true_directions, player)
            self.is_valid = True
            return self.is_valid
        return

    def compile_valid_moves(self, player, opponent):
        for i in range(len(self.board.mat)):
            for j in range(len(self.board.mat[0])):
                if self.board.mat[i][j] == 0:
                    if self.is_valid_move(self.board, i, j, player, opponent):
                        self.valid_moves.append((i, j))
        return self.valid_moves

    def get_best_move(self, valid_moves, board):
        for move in valid_moves:
            test_board = deepcopy(board)
            self.make_move(test_board, move[0], move[1], self.curr_player)
            scores = self.sum_player_pts(test_board)
            difference = scores[1] - scores[0]
            index = valid_moves.index(move)
            valid_moves[index] = [move[0], move[1], difference]
            best_move = max(valid_moves, key=lambda x:x[2])
        return best_move[0], best_move[1]

    def sum_player_pts(self, board: Board):
        """ Method keeps track of the by iterating over the game board and
        summing totals.
        
            Return: Tuple containing the score for Player X and Player 0.
        """
        player_1_pts = 0        # Player 1 is will always be the human player.
        player_2_pts = 0        # Player 2 will be either human or AI.

        # Iterates over the entire board matrix and returns the player point totals.
        for i in range(board.size):
            for j in range(board.size):
                if board.mat[i][j] == 1:
                    player_1_pts += 1
                elif board.mat[i][j] == 2:
                    player_2_pts += 1
                
                # Since values 2 and 3 will never be on the board at the same time
                # we can use the same player_2_pts variable in this statement.
                elif board.mat[i][j] == 3:
                    player_2_pts += 1
        return (player_1_pts, player_2_pts)
