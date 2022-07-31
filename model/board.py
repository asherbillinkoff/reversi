from model.players import Player

class Board():
    """ This class is responsible for generating the Reversi board and storing the 
    status of the board through the game. Also responisble for getting, setting and
    updating board state based on previous move."""

    EMPTY_CELL = 0

    def __init__(self, size=8):
        """ Initializes the board class by setting the board size and placing the
        starting pieces in the center of the board."""
        self.size = size
        # Create a matrix of zeroes for the Reversi board
        self.mat = [[self.EMPTY_CELL] * size for _ in range(size)]
        self.mat[size // 2 - 1][size // 2 - 1] = Player.X
        self.mat[size // 2][size // 2] = Player.X
        self.mat[size // 2 - 1][size // 2] = Player.O
        self.mat[size // 2][size // 2 - 1] = Player.O

    def get_cell(self, row, col):
        """ Returns the requested cell value after accessing the board.

            Args:
                row (int): Cell value for a given row.
                col (int): Cell value for a given column.

            Returns:
                int: Value found for given cell (0 = empty, 1 = Player X, 2 = Player O)
        """
        return self.mat[row][col]

    def update_cell(self, row, col, player):
        """ Updates given cell after player has made a valid move.

            Args:
                row (int): Cell value for a given row.
                col (int): Cell value for a given column.
                player (int enum): Current player value.

            Returns:
                None
        """
        self.mat[row][col] = player
        
    def update_board(self, row, col, directions, player):
        """ Once a valid move has been executed this method .

            Args:
                row (int): Cell value for a given row.
                col (int): Cell value for a given column.
                directions (list): A list containing directions where valid moves exist.
                player (int enum): Current player value.

            Returns:
                bool: Returns True if board has been updated successfully
        """
        self.opponent = 3 - player
        for direction in directions:
            while self.mat[row + direction[0]][col + direction[1]] == self.opponent:
                self.mat[row + direction[0]][col + direction[1]] = player
                row += direction[0]
                col += direction[1]
        return True

