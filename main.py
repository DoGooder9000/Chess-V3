import pygame
import copy

pygame.init()


class Piece:
    def __init__(self, FEN: str, color: str, board_pos: tuple[int]):
        self.FEN = FEN
        self.color = color
        self.board_pos = board_pos


class Move:
    def __init__(self, start_square: tuple[int], target_square: tuple[int]):
        self.start_square = start_square
        self.target_square = target_square


class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        
        self.size = (width, height)
        
    
    def Draw(self):
        pass




window_size = (300, 300)
window_width, window_height = window_size
window_name = "Chess V3"

window = pygame.display.set_mode(window_size)
pygame.display.set_caption(window_name)


board_size = (8, 8)
board_width, board_height = board_size

square_width = window_width/board_width
square_height = window_height/board_height
square_size = (square_width, square_height)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

