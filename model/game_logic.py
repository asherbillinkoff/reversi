from copy import deepcopy

from model.board import Board
from model.player import Player
from model.ai_player import AIPlayer


class GameLogic:
    def __init__(self, players):
        self.is_valid = False


    def is_valid_move(self, board: Board, row, col, player: Player, opponent: Player):
        """    Function determines if the user move is valid based on a series of
        checks. It checks if the cell is on the board, if it's empty, if there are
        adjacent opponent disks and if those adjacent disks have any of the current
        player's disks on the other side (i.e. any complete disk sandwiches).

            Returns:
                true_directions: list of valid directions for moves for a given move.
        """

        # Create a list of all directions in which a valid move exists.
        true_directions = []
        self.is_valid = False
        
        # Valid move condition #1: the cell is empty.
        if board.get_cell(row, col) == 0:
            directions = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
            cell = (row, col)
            
            # Increment user move in all directions to confirm where the valid
            # moves are.
            for direction in directions:
                check_cell = (row + direction[0], col + direction[1])

                # Check to make sure the incremented index is in range of our board.
                if max(check_cell) >= board.size or min(check_cell) < 0:
                    continue

                # Valid move condition #2: there is an adjacent cell with the
                # other player's disk.
                if board.mat[check_cell[0]][check_cell[1]] == opponent.symbol:

                    # Increment the current cell in that direction.
                    cell = (cell[0] + direction[0], cell[1] + direction[1])
                    if max(cell) >= board.size or min(cell) < 0:
                        continue

                    # Valid move condition #3: the given direction contains
                    # another one of current player's disks further down the
                    # row (i.e. there is a valid disk sandwich).
                    next_cell = cell
                    while board.mat[next_cell[0]][next_cell[1]] == opponent.symbol:
                        next_cell = (next_cell[0] + direction[0],
                                    next_cell[1] + direction[1])

                        # Make sure that the incremented cell is still within
                        # board range.
                        if max(next_cell) >= board.size or min(next_cell) < 0:
                            self.is_valid = False
                            break
                        # If incremented cell is = player then move is valid.
                        elif board.mat[next_cell[0]][next_cell[1]] == player.symbol:
                            self.is_valid = True
                            break
                            
                    # When code reaches the end of the disk sandwich, it appends
                    # that direction to a list.
                    if self.is_valid:
                        true_directions.append(direction)    
                cell = (row, col)
                self.is_valid = False
        else:
            return

        # Confirm if any valid directions exist for user move.
        if true_directions != []:
            self.is_valid = True
            return true_directions
        return

    def compile_valid_moves(self, board, player, opponent):
        """    Method iterates over the entire board and places all valid moves as 
            keys into a dictionary with the associated 'true_directions' as values
            which are passed along from the is_valid_move function.

            Returns:
                valid_moves: dictionary containing the move locations as keys and
                            the directions of valid moves as values.
        """
        
        test_board = deepcopy(board)
        valid_moves = {}
        for i in range(len(test_board.mat)):
            for j in range(len(test_board.mat[0])):
                if test_board.mat[i][j] == 0:
                    if self.is_valid_move(test_board, i, j, player, opponent):

                        # The method passes along the valid move directions for 
                        # each associated move.
                        valid_moves[(i, j)] = self.is_valid_move(test_board, i, j, player, opponent)
        return valid_moves

    def sum_player_pts(self, board: Board):
        """    Method keeps track of the by iterating over the game board and
        summing totals.

            Returns:
                tuple: Contains the value of first and second player points.
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

    def make_move(self, board: Board, row, col, directions, player: Player):
        """    Method pass along a user move to the board to be updated.
        """
        
        board.update_board(row, col, directions, player)

    def choose_move(self, board, depth, player: Player, opponent: Player):
        test_board = deepcopy(board)

        # Find all the valid moves
        valid_moves = self.compile_valid_moves(board, player, opponent)
        board_values = []
        for move in valid_moves.keys():
            directions = valid_moves[move]
            self.make_move(test_board, move[0], move[1], directions, player)
            move_value = self.minimax(test_board, depth, opponent, player) # swapped oppnent and player here for testing
            board_values.append((move_value, move[0], move[1]))
            test_board = deepcopy(board)
        if len(board_values) == 0:
            row, col = None, None
        else:
            best_move = max(board_values, key=lambda x: x[0])
            row = best_move[1]
            col = best_move[2]
        return (row, col)

    def minimax(self, board, depth, max_player, min_player):
        # Check if board is in terminal state.
        moves_remaining = self.compile_valid_moves(board, max_player, min_player)
        if moves_remaining is None:      # This logic may be insufficient
            score = self.sum_player_pts(board)
            if score[1] > score[0]:
                return 1
            elif score[0] > score[1]:
                return -1
            elif score[0] == score[1]:
                return 0

        # Heuristic function here will return the number of valid moves remaining
        # as it's utility value.
        elif depth == 0:
            return len(moves_remaining)

        minimax_values = []
        for move in moves_remaining.keys():
            test_board = deepcopy(board)
            if max(move) >= board.size or min(move) < 0:
                    continue
            directions = moves_remaining[move]
            self.make_move(test_board, move[0], move[1], directions, max_player)
            board_value = self.minimax(test_board, depth - 1, min_player, max_player)
            minimax_values.append(board_value)
        
        if len(minimax_values) == 0:
            return 0
        if isinstance(max_player, AIPlayer):
            return max(minimax_values)
        else:
            return min(minimax_values)


