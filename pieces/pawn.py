import pygame
from piece import Piece

class Pawn(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        img_path = f"assets/pieces/{color}_pawn.png"
        self.image = pygame.image.load(img_path)
        self.first_move = True
        self.en_passant_vulnerable = False

    def get_valid_moves(self, board):
        moves = []
        dir = -1 if self.color == "white" else 1
        
        if self.row + dir >= 0 and self.row + dir < 8:
            # Check forward move
            if not board.get_piece(self.row + dir, self.col):
                moves.append((self.row + dir, self.col))

                # Check two steps forward on first move
                if self.first_move and not board.get_piece(self.row + 2*dir, self.col) and self.row + 2*dir >= 0 and self.row + 2*dir < 8:
                    moves.append((self.row + 2*dir, self.col))
                    # Mark as vulnerable to en passant
                    self.en_passant_vulnerable = True
            
            # Check attack moves
            for col_dir in [-1, 1]:
                if self.col + col_dir >= 0 and self.col + col_dir < 8:
                    # Normal capture
                    piece = board.get_piece(self.row + dir, self.col + col_dir)
                    if piece and piece.color != self.color:
                        moves.append((self.row + dir, self.col + col_dir))
                    
                    # En passant
                    en_passant_piece = board.get_piece(self.row, self.col + col_dir)
                    if en_passant_piece and en_passant_piece.color != self.color and isinstance(en_passant_piece, Pawn):
                        if en_passant_piece.en_passant_vulnerable:
                            moves.append((self.row + dir, self.col + col_dir))

        return moves

    def move(self, row, col):
        self.first_move = False
        self.en_passant_vulnerable = False
        super().move(row, col)