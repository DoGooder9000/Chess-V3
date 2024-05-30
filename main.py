import pygame
import copy

pygame.init()


class Piece:
	def __init__(self, FEN: str, color: str, board_pos: tuple[int]):
		self.FEN = FEN
		self.color = color
		self.board_pos = board_pos
		
		self.SetRect()
		
	def SetRect(self):
		self.rect = pygame.Rect((self.board_pos[0]*square_width, self.board_pos[1]*square_height), square_size)
	
	def Draw(self):
		img = None
		
		match self.FEN:
			
			case 'p':
				img = BlackPawn
				
			case 'r':
				img = BlackRook
				
			case 'n':
				img = BlackKnight
				
			case 'b':
				img = BlackBishop
				
			case 'q':
				img = BlackQueen
				
			case 'k':
				img = BlackKing

			case 'P':
				img = WhitePawn
			
			case 'R':
				img = WhiteRook
				
			case 'N':
				img = WhiteKnight
				
			case 'B':
				img = WhiteBishop
				
			case 'Q':
				img = WhiteQueen
			
			case 'K':
				img = WhiteKing
				
		window.blit(img, self.rect.topleft)


class Rook(Piece):
	def __init__(self, color: str, board_pos: tuple[int]):
		if color == 'White':
			FEN = 'R'
		else:
			FEN = 'r'
		
		super().__init__(FEN, color, board_pos)

class Bishop(Piece):
	def __init__(self, color: str, board_pos: tuple[int]):
		if color == 'White':
			FEN = 'B'
		else:
			FEN = 'b'
		
		super().__init__(FEN, color, board_pos)

class Knight(Piece):
	def __init__(self, color: str, board_pos: tuple[int]):
		if color == 'White':
			FEN = 'N'
		else:
			FEN = 'n'
		
		super().__init__(FEN, color, board_pos)

class Queen(Piece):
	def __init__(self, color: str, board_pos: tuple[int]):
		if color == 'White':
			FEN = 'Q'
		else:
			FEN = 'q'
		
		super().__init__(FEN, color, board_pos)

class King(Piece):
	def __init__(self, color: str, board_pos: tuple[int]):
		if color == 'White':
			FEN = 'K'
		else:
			FEN = 'k'
		
		super().__init__(FEN, color, board_pos)

class Pawn(Piece):
	def __init__(self, color: str, board_pos: tuple[int]):
		if color == 'White':
			FEN = 'P'
		else:
			FEN = 'p'
		
		super().__init__(FEN, color, board_pos)


class Move:
	def __init__(self, start_square: tuple[int], target_square: tuple[int]):
		self.start_square = start_square
		self.target_square = target_square


class Board:
	def __init__(self, width: int, height: int, start_color: str = 'White'):
		self.width = width
		self.height = height
		
		self.size = (width, height)

		self.color = start_color
		
		self.board = []

		self.Reset()
	
	def Reset(self):
		self.GenerateNewBoard()
	
	def GenerateNewBoard(self, FEN: str = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'):
		self.board = []

		for _ in range(self.width * self.height):
			self.board.append(0)

		i = 0 # Index in the board we are at
		
		for symbol in FEN:
			match symbol:
				case 'R':
					self.board[i] = Rook('White', IndexToBoardPos(i))
					i += 1
					
				case 'r':
					self.board[i] = Rook('Black', IndexToBoardPos(i))
					i += 1
					
				case 'N':
					self.board[i] = Knight('White', IndexToBoardPos(i))
					i += 1
					
				case 'n':
					self.board[i] = Knight('Black', IndexToBoardPos(i))
					i += 1
				
				case 'B':
					self.board[i] = Bishop('White', IndexToBoardPos(i))
					i += 1
					
				case 'b':
					self.board[i] = Bishop('Black', IndexToBoardPos(i))
					i += 1
				
				case 'Q':
					self.board[i] = Queen('White', IndexToBoardPos(i))
					i += 1
					
				case 'q':
					self.board[i] = Queen('Black', IndexToBoardPos(i))
					i += 1
				
				case 'K':
					self.board[i] = King('White', IndexToBoardPos(i))
					i += 1
					
				case 'k':
					self.board[i] = King('Black', IndexToBoardPos(i))
					i += 1
				
				case 'P':
					self.board[i] = Pawn('White', IndexToBoardPos(i))
					i += 1
					
				case 'p':
					self.board[i] = Pawn('Black', IndexToBoardPos(i))
					i += 1
				
				case '/':
					continue
				
				case _:
					if symbol in '12345678':
						for j in range(int(symbol)):
							self.board[i] = '_'
							i += 1
		
	
	def Draw(self) -> None:
		for x in range(board_width):
			for y in range(board_height):
				if (x+y)%2 == 0:
					pygame.draw.rect(window, LightSquareColor, pygame.Rect((x*square_width, y*square_height), square_size))
				else:
					pygame.draw.rect(window, DarkSquareColor, pygame.Rect((x*square_width, y*square_height), square_size))

def GetPieceBoardPos(board_pos: tuple[int], board: Board):
	return board.board[BoardPosToIndex(board_pos)]

def BoardPosToIndex(pos: tuple) -> int:
	return pos[0] + pos[1] * board_width

def IndexToBoardPos(index: int) -> tuple[int]:
	return (index%board_width, index//board_width)

def MouseToBoardPos(mouse_pos: tuple[float]):
	rank = int(mouse_pos[0]//square_width)
	file = int(mouse_pos[1]//square_height)

	return (rank, file)

def DrawPieces(board: Board):
	for piece in board.board:
		if piece != '_':
			piece.Draw()

def Update():
	pygame.display.update()

window_size = (800, 800)
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



currentBoard = Board(board_width, board_height, 'White')

mouseDown = False

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()

		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouseDown = True

			square_loc = MouseToBoardPos(pygame.mouse.get_pos())

			clickedPiece = GetPieceBoardPos(square_loc, currentBoard)

			if clickedPiece == '_':
				clickedPiece = None
			
			elif clickedPiece.color != currentBoard.color:
				clickedPiece = None

		elif event.type == pygame.MOUSEBUTTONUP:
			mouseDown = False
			
		elif event.type == pygame.MOUSEMOTION:
			pass
	
	window.fill('black')
	
	currentBoard.Draw()
	
	DrawPieces(currentBoard)
	
	Update()

