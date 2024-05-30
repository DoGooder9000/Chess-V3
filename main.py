import pygame
import copy

pygame.init()

class Move:
	pass

class Piece:
	pass

class Board:
	pass

class Piece:
	def __init__(self, FEN: str, color: str, board_pos: tuple[int]):
		self.FEN = FEN
		self.color = color
		self.board_pos = board_pos

		self.IndexDirections = IndexDirections = {'Top Left':-9, 'Up':-8, 'Top Right':-7, 'Right':+1, 'Bottom Right':+9, 'Down':+8, 'Bottom Left':+7, 'Left':-1}
		
		self.SetRect()
		
	def SetRect(self):
		self.rect = pygame.Rect((self.board_pos[0]*square_width, self.board_pos[1]*square_height), square_size)

	def SetBoardPos(self, board_pos: tuple[int]):
		self.board_pos = board_pos
		self.SetRect()
	
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
	
	def GetLegalMoves(self) -> list[Move]:
		pass


class Rook(Piece):
	def __init__(self, color: str, board_pos: tuple[int]):
		if color == 'White':
			FEN = 'R'
		else:
			FEN = 'r'

		self.RookDirections = ['Up', 'Down', 'Left', 'Right']
		
		super().__init__(FEN, color, board_pos)
	
	def GetLegalMoves(self, board: Board) -> list[Move]:
		LegalMoves = []

		for direction in self.RookDirections: # Loop through all directions
			index = BoardPosToIndex(self.board_pos)

			for i in range(GetNumberOfSquaresToEdge(self.board_pos, direction)+1): # Step in each direction
				if i == 0: # Skip ourselves
					continue
					
				index += self.IndexDirections[direction]

				if board.board[index] == '_': # If the square is blank, it is a legal move
					LegalMoves.append(Move(self.board_pos, IndexToBoardPos(index), self))
					continue

				elif board.board[index].color == self.color: # If we run into our own piece, switch to another direction
					break
				
				else: # This is just if the piece is an enemy piece, we can capture, but cant go further
					LegalMoves.append(self.board_pos, IndexToBoardPos(index), self)
					break

		return LegalMoves
	
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
	def __init__(self, start_square: tuple[int], target_square: tuple[int], pieceMoving: Piece, isEnPassant = False) -> None:
		self.start_square = start_square
		self.target_square = target_square
		self.piece = pieceMoving
		self.isEnPassant = isEnPassant


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
	
	def SetPieceAtBoardPos(self, board_pos: tuple[int], value: any):
		self.board[BoardPosToIndex(board_pos)] = value
	
	def Move(self, move: Move):
		self.SetPieceAtBoardPos(move.start_square, '_')
		self.SetPieceAtBoardPos(move.target_square, move.piece)
		move.piece.SetBoardPos(move.target_square)

		ChangePlayColor(self)





def GetNumberOfSquaresToEdge(start_square: tuple[int], dir: str): # 8 Different directions: Up = -8, Down = +8, Left = -1, Right = +1, Top Right = -7, Top Left = -9, Bottom Right = +9, Bottom Left = +7
	X, Y = start_square
	
	l = X
	r = (board_width - 1) - X
	u = Y
	d = (board_height - 1) - Y

	if dir == 'Left':
		return l

	if dir == 'Right':
		return r
	
	if dir == 'Up':
		return u
	
	if dir == 'Down':
		return d
	
	if dir == 'Top Left':
		return min(u, l)
	
	if dir == 'Top Right':
		return min(u, r)
	
	if dir == 'Bottom Left':
		return min(d, l)
	
	if dir == 'Bottom Right':
		return min(d, r)
	
	
	return


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

def GetBoardPosFromPiece(piece: Piece, board: Board):
	index = 0

	for otherPiece in board.board:
		if otherPiece == piece:
			return IndexToBoardPos(index)

		index += 1

def DrawPieces(board: Board, DrawClickedPiece = True):
	global clickedPiece


	for piece in board.board:
		if piece != '_':
			if DrawClickedPiece:
				if piece != clickedPiece:
					piece.Draw()
			else:
				piece.Draw()
	
	if clickedPiece != None and DrawClickedPiece:
		clickedPiece.Draw()

def ChangePlayColor(board: Board):
	if board.color == 'White': board.color = 'Black'
	else: board.color = 'White'

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

clickedPiece: Piece = None

mouseDown = False

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()

		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouseDown = True

			start_square = MouseToBoardPos(pygame.mouse.get_pos())

			clickedPiece = GetPieceBoardPos(start_square, currentBoard)

			if clickedPiece == '_':
				clickedPiece = None
			
			elif clickedPiece.color != currentBoard.color:
				clickedPiece = None

		elif event.type == pygame.MOUSEBUTTONUP:
			mouseDown = False

			if clickedPiece != None:
				target_square = MouseToBoardPos(pygame.mouse.get_pos())
				start_square = GetBoardPosFromPiece(clickedPiece, currentBoard)

				if target_square != start_square:
					currentBoard.Move(Move(start_square, target_square, clickedPiece))
				
				else:
					clickedPiece.SetBoardPos(start_square)
			
			clickedPiece = None
			
		elif event.type == pygame.MOUSEMOTION:
			if mouseDown and clickedPiece != None:
				clickedPiece.rect.center = pygame.mouse.get_pos()
	
	window.fill('black')
	
	currentBoard.Draw()
	
	DrawPieces(currentBoard)
	
	Update()