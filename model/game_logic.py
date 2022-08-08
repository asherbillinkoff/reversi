from copy import deepcopy

from model.board import Board
from model.player import Player


class GameLogic:
    def __init__(self, board: Board, players):
        self.board = board
        self.is_valid = False
        self.curr_player = players[0]
        self.opponent = players[1]

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
        if self.board.get_cell(row, col) == 0:
            directions = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
            cell = (row, col)
            
            # Increment user move in all directions to confirm where the valid
            # moves are.
            for direction in directions:
                check_cell = (row + direction[0], col + direction[1])

                # Check to make sure the incremented index is in range of our board.
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

    def compile_valid_moves(self, player, opponent):
        """    Method iterates over the entire board and places all valid moves as 
            keys into a dictionary with the associated 'true_directions' as values
            which are passed along from the is_valid_move function.

            Returns:
                valid_moves: dictionary containing the move locations as keys and
                            the directions of valid moves as values.
        """
        
        test_board = deepcopy(self.board)
        valid_moves = {}
        for i in range(len(self.board.mat)):
            for j in range(len(self.board.mat[0])):
                if self.board.mat[i][j] == 0:
                    if self.is_valid_move(test_board, i, j, player, opponent):

                        # The method passes along the valid move directions for 
                        # each associated move.
                        valid_moves[(i, j)] = self.is_valid_move(test_board, i, j, player, opponent)
        return valid_moves

    def get_best_move(self, valid_moves):
        """    Method iterates over the list of valid moves and places them on a 
        test board to then compute the score of the possible move. The move 
        scores are then summed into a list of lists. The inner lists contain 
        [row, col, move_score].

            Args:
                valid_moves (dict): Dictionary containing the move locations as keys and
                                    the directions of valid moves as values.

            Returns:
                row: The row of the best available move.
                col: The col of the best available move.
        """
        
        for move in valid_moves:
            test_board = deepcopy(self.board)
            directions = valid_moves[move]

            # Make the valid move on the test board to compute the score.
            self.make_move(test_board, move[0], move[1], directions, self.curr_player)
            scores = self.sum_player_pts(test_board)
            difference = scores[1] - scores[0]
            
            # Add the move and associated score difference as values in the dictionary.
            valid_moves[move] = [move[0], move[1], difference]
            test_board = []

        # Find the max move_score and return it.    
        best_move = max(list(valid_moves.values()), key=lambda x:x[2])
        return best_move[0], best_move[1]

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

    def choose_move(self, board, depth):
        test_board = deepcopy(board)

        # Find all the valid moves
        valid_moves = self.compile_valid_moves(self.curr_player, self.opponent)
        board_values = []
        for move in valid_moves.keys():
            directions = valid_moves[move]
            self.make_move(test_board, move[0], move[1], directions, self.curr_player)
            move_value = self.minimax(test_board, depth, self.curr_player, self.opponent)
            board_values.append(move_value)
        return max(board_values)

    def minimax(self, board, depth, max_player, min_player):
        # Check if board is in terminal state.
        remaining_moves_max_player = self.compile_valid_moves(max_player, min_player)
        if remaining_moves_max_player is None:      # This logic may be insufficient
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
            valid_moves_utility = self.compile_valid_moves(max_player, min_player)
            return len(valid_moves_utility)

        test_board = deepcopy(board)
        values = []
        valid_moves = self.compile_valid_moves(self.curr_player, self.opponent)
        for move in valid_moves.keys():
            directions = valid_moves[move]
            self.make_move(test_board, move[0], move[1], directions, self.curr_player)
            board_value = self.minimax(test_board, self.curr_player, self.opponent)
            values.append(board_value)
        
        if self.curr_player == max_player:
            return max(values)
        else:
            return min(values)


