import pygame
from piece import Piece


class Knight(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        img_path = f"assets/pieces/{color}_knight.png"
        self.image = pygame.image.load(img_path)

    def get_valid_moves(self, board):
        moves = []
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        for row_dir, col_dir in knight_moves:
            new_row = self.row + row_dir
            new_col = self.col + col_dir
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = board.get_piece(new_row, new_col)
                if not target_piece or target_piece.color != self.color:
                    moves.append((new_row, new_col))
        return moves