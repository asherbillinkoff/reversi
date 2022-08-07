from model.board import Board
from view.board_view import BoardView


class BoardConsoleView(BoardView):
  '''Class is responsible for drawing the board from the current state in the model, for viewing by the user.
  The board size is inherited from the board object.'''

  symbols = {0: ' ', 1: 'X', 2: 'O', 3: 'I'}
  def __init__(self, board: Board):
    super().__init__(board)

  def draw_board(self):
    board_size = self.board.size
    header = '+'

    # Appending column numbers to the head for easier game visibility.
    for i in range(board_size):
      header += ' ' + str(i) + ' +'
    # header ='+' + '---+' * (board_size)           # Old code for implementing clean header.
    print(header)
    for i in range(board_size):
      for j in range(board_size):
        cell = self.board.get_cell(i, j)
        print(f'| {self.symbols[cell]} ', end='')
      print(i)                                      # Prints the row number.
    print(header)





