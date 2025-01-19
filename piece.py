import pygame
from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.selected = False
        self.image = None

    @abstractmethod
    def get_valid_moves(self, board):
        pass

    def draw(self, win, sq_size):
        if self.image is not None:
            piece_img = pygame.transform.scale(self.image, (sq_size, sq_size))
            win.blit(piece_img, (self.col * sq_size, self.row * sq_size))

    def move(self, row, col):
        self.row = row
        self.col = col

    def __repr__(self):
        return f"{self.color} {self.__class__.__name__}"