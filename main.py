import pygame
from board import Board
from computer import Computer

# Constants
WIDTH, HEIGHT = 600, 600
SQ_SIZE = WIDTH // 8
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (255, 255, 0)

def draw_highlight(win, board):
  selected_piece = board.get_selected_piece()
  if not selected_piece:
    return
  
  moves = selected_piece.get_valid_moves(board)
  for row,col in moves:
    x = col * SQ_SIZE
    y = row * SQ_SIZE
    pygame.draw.rect(win, HIGHLIGHT_COLOR, (x,y, SQ_SIZE, SQ_SIZE), 3)

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game")
    clock = pygame.time.Clock()

    board = Board()
    computer = Computer("black")
    player_turn = "white"

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and player_turn == "white":
              x, y = event.pos
              col = x // SQ_SIZE
              row = y // SQ_SIZE

              # Check if select piece or move piece
              selected_piece = board.get_selected_piece()
              if not selected_piece:
                  # Select a new piece
                  board.select_piece(row, col)
              else:
                moves = selected_piece.get_valid_moves(board)
                if (row,col) in moves:
                  board.move_piece(selected_piece.row, selected_piece.col, row, col)
                  board.selected_piece = None
                  player_turn = "black"
                else:
                  board.select_piece(row, col)

        if player_turn == "black":
           move = computer.get_move(board)
           if move:
             board.move_piece(move[0], move[1], move[2], move[3])
             player_turn = "white"

        # Check Checkmate
        if board.is_checkmate("white"):
          print("Black Wins! Checkmate")
          running = False
        elif board.is_checkmate("black"):
          print("White Wins! Checkmate")
          running = False
        elif board.is_stalemate("white") or board.is_stalemate("black"):
            print("Stalemate! Game Draw.")
            running = False
        elif board.has_insufficient_material():
           print("Insufficient Material! Game Draw")
           running = False

        # Draw board and pieces
        board.draw_squares(win, SQ_SIZE)
        board.draw_pieces(win, SQ_SIZE)
        draw_highlight(win, board)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()