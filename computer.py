import random

class Computer:
    def __init__(self, color):
        self.color = color

    def get_move(self, board):
      # Get all possible moves for the computer
      all_moves = board.get_all_moves(self.color)
      if not all_moves:
          return None
      # Chose a random move for now
      return random.choice(all_moves)