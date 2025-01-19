import pygame
from piece import Piece


class Rook(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        img_path = f"assets/pieces/{color}_rook.png"
        self.image = pygame.image.load(img_path)

    def get_valid_moves(self, board):
        moves = []
        # Define directions: Up, Down, Left, Right
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for row_dir, col_dir in directions:
            row, col = self.row, self.col
            while True:
                row += row_dir
                col += col_dir
                if row < 0 or row >= 8 or col < 0 or col >= 8:
                    break
                piece = board.get_piece(row, col)
                if not piece:
                    moves.append((row, col))
                else:
                    if piece.color != self.color:
                        moves.append((row, col))
                    break
        return moves