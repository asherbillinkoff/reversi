from model.player import Player

class Board():
    """ This class is responsible for generating the Reversi board and storing the 
    status of the board through the game. Also responisble for getting, setting and
    updating board state based on user move."""

    EMPTY_CELL = 0

    def __init__(self, size=8):
        """ Initializes the board class by setting the board size and placing the
        starting pieces in the center of the board."""
        self.size = size

        # Create a matrix of zeroes for the Reversi board.
        self.mat = [[self.EMPTY_CELL] * size for _ in range(size)]

    def place_starting_pieces(self, player1: Player, player2: Player):
        # Initialize starting pieces on the board for given players.
        self.mat[self.size // 2 - 1][self.size // 2 - 1] = player1.symbol
        self.mat[self.size // 2][self.size // 2] = player1.symbol
        self.mat[self.size // 2 - 1][self.size // 2] = player2.symbol
        self.mat[self.size // 2][self.size // 2 - 1] = player2.symbol

    def get_cell(self, row, col):
        """ Returns the requested cell value after accessing the board."""

        return self.mat[row][col]

    def update_cell(self, row, col, symbol):
        """ Updates given cell after player has made a valid move."""

        self.mat[row][col] = symbol
        
    def update_board(self, row, col, directions, player: Player):
        """ Once a valid move has been found this method will update all the
        corresponding disks."""

        original_row, original_col = row, col
        for direction in directions:
            row, col = original_row, original_col
            self.mat[row][col] = 0
            while self.mat[row][col] != player.symbol:
                self.mat[row][col] = player.symbol
                row += direction[0]
                col += direction[1]
        self.mat[original_row][original_col] = player.symbol
        return True

