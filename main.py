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
        for x in range(board_width):
            for y in range(board_height):
                if (x+y)%2 == 0:
                    pygame.draw.rect(window, LightSquareColor, pygame.Rect((x*square_width, y*square_height), square_size))
                else:
                    pygame.draw.rect(window, DarkSquareColor, pygame.Rect((x*square_width, y*square_height), square_size))


def Update():
    pygame.display.update()

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
                                     
LightSquareColor = (209, 162, 96)
DarkSquareColor = (115, 90, 56)


WhiteKing = pygame.transform.scale(pygame.image.load('Images/whiteking.png'), square_size)
BlackKing = pygame.transform.scale(pygame.image.load('Images/blackking.png'), square_size)

WhiteQueen = pygame.transform.scale(pygame.image.load('Images/whitequeen.png'), square_size)
BlackQueen = pygame.transform.scale(pygame.image.load('Images/blackqueen.png'), square_size)

WhiteKnight = pygame.transform.scale(pygame.image.load('Images/whiteknight.png'), square_size)
BlackKnight = pygame.transform.scale(pygame.image.load('Images/blackknight.png'), square_size)

WhiteBishop = pygame.transform.scale(pygame.image.load('Images/whitebishop.png'), square_size)
BlackBishop = pygame.transform.scale(pygame.image.load('Images/blackbishop.png'), square_size)

WhiteRook = pygame.transform.scale(pygame.image.load('Images/whiterook.png'), square_size)
BlackRook = pygame.transform.scale(pygame.image.load('Images/blackrook.png'), square_size)

WhitePawn = pygame.transform.scale(pygame.image.load('Images/whitepawn.png'), square_size)
BlackPawn = pygame.transform.scale(pygame.image.load('Images/blackpawn.png'), square_size)



Board = Board(8, 8)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    window.fill('black')
    
    Board.Draw()
    Update()

