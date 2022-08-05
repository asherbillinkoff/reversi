from model.symbols import Symbols

class Board():
    """ This class is responsible for generating the Reversi board and storing the 
    status of the board through the game. Also responisble for getting, setting and
    updating board state based on user move."""

    EMPTY_CELL = 0

    def __init__(self, size=8):
        """ Initializes the board class by setting the board size and placing the
        starting pieces in the center of the board."""
        self.size = size
        # Create a matrix of zeroes for the Reversi board
        self.mat = [[self.EMPTY_CELL] * size for _ in range(size)]

        # Board for testing end of game sequencing
        # self.mat = [[Player.O,0,Player.O,Player.X],
        #             [Player.O,Player.O,Player.O,Player.O],
        #             [Player.O,Player.O,Player.O,Player.O],
        #             [Player.O,Player.X,Player.O,Player.O]]

    def get_cell(self, row, col):
        """ Returns the requested cell value after accessing the board."""

        return self.mat[row][col]

    def update_cell(self, row, col, player):
        """ Updates given cell after player has made a valid move."""

        self.mat[row][col] = player
        
    def update_board(self, row, col, directions, player):
        """ Once a valid move has been found this method will update all the
        corresponding disks."""

        original_row = row
        original_col = col
        for direction in directions:
            row = original_row
            col = original_col
            self.mat[row][col] = 0
            while self.mat[row][col] != player:
                self.mat[row][col] = player
                row += direction[0]
                col += direction[1]
        return True

