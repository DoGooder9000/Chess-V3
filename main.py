import pygame
import copy

pygame.init()


class Piece:
    def __init__(self):
        pass


class Move:
    def __init__(self, start_square: tuple[int], target_square: tuple[int]):
        self.start_square = start_square
        self.target_square = target_square






window_size = (600, 600)
window_width, window_height = window_size
window_name = "Chess V3"

window = pygame.display.set_mode(window_size)
pygame.display.set_caption(window_name)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

