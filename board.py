import pygame
from pieces.pawn import Pawn
from pieces.rook import Rook
from pieces.knight import Knight
from pieces.bishop import Bishop
from pieces.queen import Queen
from pieces.king import King

class Board:
    def __init__(self):
        self.board = self.reset_board()
        self.selected_piece = None
        self.last_move = None

    def reset_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]

        # Initialize Black Pieces
        board[0][0] = Rook("black", 0, 0)
        board[0][1] = Knight("black", 0, 1)
        board[0][2] = Bishop("black", 0, 2)
        board[0][3] = Queen("black", 0, 3)
        board[0][4] = King("black", 0, 4)
        board[0][5] = Bishop("black", 0, 5)
        board[0][6] = Knight("black", 0, 6)
        board[0][7] = Rook("black", 0, 7)
        for col in range(8):
            board[1][col] = Pawn("black", 1, col)
        
        # Initialize White Pieces
        board[7][0] = Rook("white", 7, 0)
        board[7][1] = Knight("white", 7, 1)
        board[7][2] = Bishop("white", 7, 2)
        board[7][3] = Queen("white", 7, 3)
        board[7][4] = King("white", 7, 4)
        board[7][5] = Bishop("white", 7, 5)
        board[7][6] = Knight("white", 7, 6)
        board[7][7] = Rook("white", 7, 7)
        for col in range(8):
            board[6][col] = Pawn("white", 6, col)
        return board

    def draw_squares(self, win, sq_size):
        colors = [(240, 217, 181), (181, 136, 99)]  # Light and dark square colors
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                pygame.draw.rect(win, color, (col * sq_size, row * sq_size, sq_size, sq_size))

    def draw_pieces(self, win, sq_size):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    piece.draw(win, sq_size)

    def get_piece(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        # Get the piece to move
        piece = self.get_piece(start_row, start_col)
        if not piece:
            return False

        # Check if the move is in the piece's valid moves
        valid_moves = piece.get_valid_moves(self)
        if (end_row, end_col) not in valid_moves:
            return False

        # Simulate the move and check if it would put the king in check
        original_piece = self.board[end_row][end_col]
        self.board[start_row][start_col] = None
        self.board[end_row][end_col] = piece
        
        # Temporarily update piece's position
        original_row, original_col = piece.row, piece.col
        piece.row, piece.col = end_row, end_col

        # Check if the move puts the king in check
        is_valid = not self.is_check(piece.color)

        # Undo the move
        self.board[start_row][start_col] = piece
        self.board[end_row][end_col] = original_piece
        piece.row, piece.col = original_row, original_col

        return is_valid

    def move_piece(self, start_row, start_col, end_row, end_col):
        # Check if the move is valid
        if not self.is_valid_move(start_row, start_col, end_row, end_col):
            return False

        piece = self.get_piece(start_row, start_col)
        if piece:
            # Store the last move for potential future use
            self.last_move = (start_row, start_col, end_row, end_col)

            # Update the board
            self.board[start_row][start_col] = None
            self.board[end_row][end_col] = piece

            # Update the piece position
            piece.move(end_row, end_col)
            return True
        return False

    def select_piece(self, row, col):
        piece = self.get_piece(row, col)
        if piece:
            if self.selected_piece:
                self.selected_piece.selected = False
            self.selected_piece = piece
            piece.selected = True
            return True
        return False
    
    def get_selected_piece(self):
        return self.selected_piece
    
    def get_all_moves(self, color):
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece.color == color:
                    # Get moves that don't result in check
                    moves = [
                        move for move in piece.get_valid_moves(self)
                        if self.is_valid_move(row, col, move[0], move[1])
                    ]
                    for move in moves:
                        all_moves.append((row, col, move[0], move[1]))
        return all_moves
    
    def is_check(self, color):
        # Get position of the king
        king_row, king_col = self.find_king(color)
        if king_row is None:
            return False

        opponent_color = "black" if color == "white" else "white"
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece.color == opponent_color:
                    # Check if any opponent piece can attack the king
                    if (king_row, king_col) in piece.get_valid_moves(self):
                        return True
        return False

    def find_king(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if isinstance(piece, King) and piece.color == color:
                    return row, col
        return None, None

    def is_checkmate(self, color):
        # First, check if the king is in check
        if not self.is_check(color):
            return False
        
        # Try all possible moves to see if any can get out of check
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece.color == color:
                    for move_row, move_col in piece.get_valid_moves(self):
                        if self.is_valid_move(row, col, move_row, move_col):
                            return False
        
        return True
    
    def is_stalemate(self, color):
        # Check if the player is not in check but has no valid moves
        if self.is_check(color):
            return False
        
        return len(self.get_all_moves(color)) == 0

    def has_insufficient_material(self):
        # Expand the insufficient material check
        piece_counts = {
            "white": {"King": 0, "Queen": 0, "Rook": 0, "Bishop": 0, "Knight": 0, "Pawn": 0},
            "black": {"King": 0, "Queen": 0, "Rook": 0, "Bishop": 0, "Knight": 0, "Pawn": 0}
        }

        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece:
                    piece_counts[piece.color][piece.__class__.__name__] += 1

        # Check for scenarios with insufficient material
        for color in ["white", "black"]:
            if piece_counts[color]["Pawn"] > 0 or piece_counts[color]["Rook"] > 0 or piece_counts[color]["Queen"] > 0:
                return False
            
            # King vs King
            if piece_counts[color]["Bishop"] == 0 and piece_counts[color]["Knight"] == 0:
                continue
            
            # King and Bishop/Knight scenarios
            if (piece_counts[color]["Bishop"] <= 1 and piece_counts[color]["Knight"] <= 1 and
                piece_counts[color]["Bishop"] + piece_counts[color]["Knight"] <= 1):
                continue
            
            return False
        
        return True