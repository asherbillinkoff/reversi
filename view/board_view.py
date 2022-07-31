from abc import ABC, abstractmethod
from model.board import Board

class BoardView(ABC):
  '''Abstract class responsible for drawing the board to pass
  along to the board console view.'''
  
  def __init__(self, board: Board) -> None:
    self.board = board

  @abstractmethod
  def draw_board(self):
    pass