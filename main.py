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
		self.Directions = []
		
		self.SetRect()

	def __repr__(self) -> str:
		return f" {self.color} {self.FEN} "
		
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
	
	def GetLegalMoves(self, board: Board) -> list[Move]:
		pass

	def GetAttackedSquares(self, board: Board) -> list[tuple[int]]:
		pass


class Rook(Piece):
	def __init__(self, color: str, board_pos: tuple[int]):
		if color == 'White':
			FEN = 'R'
		else:
			FEN = 'r'
		
		super().__init__(FEN, color, board_pos)

		self.Directions = ['Up', 'Down', 'Left', 'Right']
	
	def GetLegalMoves(self, board: Board) -> list[Move]:
		return GetSlidingPieceLegalMoves(board, self)

	def GetAttackedSquares(self, board: Board) -> list[tuple[int]]:
		attacked = []

		for move in self.GetLegalMoves(board):
			attacked.append(move.target_square)
		
		return attacked
	
class Bishop(Piece):
	def __init__(self, color: str, board_pos: tuple[int]):
		if color == 'White':
			FEN = 'B'
		else:
			FEN = 'b'
		
		super().__init__(FEN, color, board_pos)

		self.Directions = ['Top Left', 'Top Right', 'Bottom Left', 'Bottom Right']

	def GetLegalMoves(self, board: Board) -> list[Move]:
		return GetSlidingPieceLegalMoves(board, self)

	def GetAttackedSquares(self, board: Board) -> list[tuple[int]]:
		attacked = []

		for move in self.GetLegalMoves(board):
			attacked.append(move.target_square)
		
		return attacked

class Knight(Piece):
	def __init__(self, color: str, board_pos: tuple[int]):
		if color == 'White':
			FEN = 'N'
		else:
			FEN = 'n'
		
		super().__init__(FEN, color, board_pos)

	def GetLegalMoves(self, board: Board) -> list[Move]:
		LegalMoves: list[Move] = []

		X, Y = self.board_pos
		index = BoardPosToIndex(self.board_pos)
		
		# Upper Moves

		if (X >= 2) and (Y >= 1):														#	#
			LegalMoves.append(Move(self.board_pos, IndexToBoardPos(index-10), self))	#	###
		
		if (X >= 1) and (Y >= 2):														#	##
			LegalMoves.append(Move(self.board_pos, IndexToBoardPos(index-17), self))	#	 #
																						#	 #

		if (X <= board_width-2) and (Y >= 2):											#	##
			LegalMoves.append(Move(self.board_pos, IndexToBoardPos(index-15), self))	#	#
																						#	#
		
		if (X <= board_width-3) and (Y >= 1):											#	  #
			LegalMoves.append(Move(self.board_pos, IndexToBoardPos(index-6), self))		#	###

		# Lower Moves
		
		if (X <= board_width-3) and (Y <= board_height-2):								#	###
			LegalMoves.append(Move(self.board_pos, IndexToBoardPos(index+10), self))	#	  #
		
		if (X <= board_width-2) and (Y <= board_height-3):								#	#
			LegalMoves.append(Move(self.board_pos, IndexToBoardPos(index+17), self))	#	#
															#	##
		
		if (X >= 1) and (Y <= board_height-2):											#	 #
			LegalMoves.append(Move(self.board_pos, IndexToBoardPos(index+15), self))	#	 #
																						#	##
		
		if (X >= 2) and (Y <= board_height-3):											#	###
			LegalMoves.append(Move(self.board_pos, IndexToBoardPos(index+6), self))		#	#


		NotOwnPieces = []

		for move in LegalMoves:

			if move.GetTargetSquarePiece(board) == '_': NotOwnPieces.append(move)
			
			else:
				if move.GetTargetSquarePiece(board).color == self.color: continue
				else: NotOwnPieces.append(move)

		return NotOwnPieces
	
	def GetAttackedSquares(self, board: Board) -> list[tuple[int]]:
		attacked = []

		for move in self.GetLegalMoves(board):
			attacked.append(move.target_square)
		
		return attacked

class Queen(Piece):
	def __init__(self, color: str, board_pos: tuple[int]):
		if color == 'White':
			FEN = 'Q'
		else:
			FEN = 'q'
		
		super().__init__(FEN, color, board_pos)

		self.Directions = ['Up', 'Down', 'Left', 'Right', 'Top Left', 'Top Right', 'Bottom Left', 'Bottom Right']
	
	def GetLegalMoves(self, board: Board) -> list[Move]:
		return GetSlidingPieceLegalMoves(board, self)

	def GetAttackedSquares(self, board: Board) -> list[tuple[int]]:
		attacked = []

		for move in self.GetLegalMoves(board):
			attacked.append(move.target_square)

		return attacked

class King(Piece):
	def __init__(self, color: str, board_pos: tuple[int]):
		if color == 'White':
			FEN = 'K'
		else:
			FEN = 'k'
		
		super().__init__(FEN, color, board_pos)
	
	def GetAttackedSquares(self, board: Board) -> list[tuple[int]]:
		return []

class Pawn(Piece):
	def __init__(self, color: str, board_pos: tuple[int]):
		if color == 'White':
			FEN = 'P'
		else:
			FEN = 'p'
		
		super().__init__(FEN, color, board_pos)

		# maybe add rank detection. If they are black and are lower than the 7th rank, they moved. Visa Versa with white

		self.moved = False
	
	def GetLegalMoves(self, board: Board) -> list[Move]:
		LegalMoves = []

		X, Y = self.board_pos
		index = BoardPosToIndex(self.board_pos)

		if self.color == 'White': # For white pawns
			# Double Pawn Push

			#	If not moved yet		And 2 spaces above is clear			And 1 space above is clear
			if self.moved == False and board.board[index-16] == '_' and board.board[index-8] == '_':
				# Make sure to set the double pawn push move argument
				LegalMoves.append(Move(self.board_pos, IndexToBoardPos(index-16), self, False, True))
			
			# Single Pawn Push
			if board.board[index-8] == '_':
				# This is only a single pawn push so no double pawn push argument
				LegalMoves.append(Move(self.board_pos, IndexToBoardPos(index-8), self))
			
			# Right and Left Captures. Remember for white, Top Left is -9, and Top Right is -7

			# Right Capture
			if board.board[index-7] != '_' and board.board[index-7].color != self.color and X <= board_width-2:
				LegalMoves.append(Move(self.board_pos, IndexToBoardPos(index-7), self))
			
			# Left Capture
			if board.board[index-9] != '_' and board.board[index-9].color != self.color and X >= 1:
				LegalMoves.append(Move(self.board_pos, IndexToBoardPos(index-9), self))

		return LegalMoves
	
	def GetAttackedSquares(self, board: Board) -> list[tuple[int]]:
		attacking = []

		X, Y = self.board_pos
		index = BoardPosToIndex(self.board_pos)

		if self.color == 'White': # White attacks the -7 (Top Right) and the -9 (Top Left)
			if X <= board_width-2: # If we are far enough away from the right side of the board
				attacking.append(IndexToBoardPos(index-7))
			
			if X >= 1: # If we are far enough away from the left side of the board
				attacking.append(IndexToBoardPos(index-9))

		else: # Black attacks the +7 (Bottom Left) and the +9 (Bottom Right)
			if X <= board_width-2:
				attacking.append(IndexToBoardPos(index+9))
			
			if X >= 1:
				attacking.append(IndexToBoardPos(index-7))

		return attacking


class Move:
	def __init__(self, start_square: tuple[int], target_square: tuple[int], pieceMoving: Piece, isEnPassant = False, isDoublePawnPush = False) -> None:
		self.start_square = start_square
		self.target_square = target_square
		self.piece = pieceMoving
		self.isEnPassant = isEnPassant
		self.isDoublePawnPush = isDoublePawnPush
	
	def __repr__(self) -> str:
		return f" {self.start_square} to {self.target_square} with {self.piece}"
	
	def __eq__(self, other: object) -> bool:
		return (self.target_square == other.target_square) and (self.start_square == other.start_square) and (self.piece == other.piece) and (self.isEnPassant == other.isEnPassant)
	
	def GetTargetSquarePiece(self, board: Board):
		return board.board[BoardPosToIndex(self.target_square)]


class Board:
	def __init__(self, width: int, height: int, start_color: str = 'White'):
		self.width = width
		self.height = height
		
		self.size = (width, height)

		self.color = start_color
		
		self.board = []

		self.DoublePawnMoves = []

		self.Reset()
	
	def Reset(self):
		self.GenerateNewBoard()
		self.DoublePawnMoves = []
	
	def GenerateNewBoard(self, FEN: str = 'rnbqkbnr/pppppppp/8/8/8/8/PPP1PPPP/RNBQKBNR'):
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
	
	def BoardMove(self, move: Move):
		# Check if the move is in the Piece's legal moves
		# Check for if the King is in check after the move, if he is, remove it

		LegalMoves = GenerateLegalMoves(self, move.piece) # This function will test the pieces moves for if they make the King get checked, and will remove them if they do

		if move in LegalMoves: # If the move is a legal move, actually play it on the board
			self.PlayMove(move) # <--- This function handles all of the internals
		
		else:
			return "No Legal Moves" # If the move is not legal, return saying it is not legal. You can't return None because the upper
									# section also is returning None currently.
	
	def PlayMove(self, move: Move): # This function is the same as the Move function, just no checking if the move is legal.
		self.DoublePawnMoves.clear()
		
		if move.isDoublePawnPush:
			self.DoublePawnMoves.append(move.piece)
		
		if type(move.piece) == Pawn:
			move.piece.moved = True

		move.piece.SetBoardPos(move.target_square) # Move the pieces board coords

		self.SetPieceAtBoardPos(move.target_square, move.piece) # Move the piece to the target square
		self.SetPieceAtBoardPos(move.start_square, '_') # Make the start square blank

		ChangePlayColor(self)


	def GetPieces(self, color: str) -> list[Piece]:
		pieces = []

		for piece in self.board:
			if piece != '_' and piece.color == color:
				pieces.append(piece)

		return pieces
	
	def GetPieceFromFEN(self, FEN: str) -> Piece:
		for piece in self.board:
			if piece != '_' and piece.FEN == FEN:
				return piece
			
		return None
	
	def GetPiece(self, piecetype: Piece, color: str) -> Piece | None:
		for piece in self.board:
			if piece != '_' and type(piece) == piecetype and piece.color == color:
				return piece
		
		return None


def GenerateLegalMoves(board: Board, piece: Piece) -> list[Move]: # This turns the psuedo legal moves into fully legal moves
	pseudoLegalMoves = piece.GetLegalMoves(board)

	fullLegalMoves = []

	if pseudoLegalMoves == None or pseudoLegalMoves == []:
		return []

	for move in pseudoLegalMoves:
		newBoard = copy.deepcopy(board)

		# We need to remake the move to reference the proper (relative) piece in the newBoard

		newMove = Move(move.start_square, move.target_square, newBoard.board[BoardPosToIndex(move.start_square)],
				 isEnPassant=move.isEnPassant, isDoublePawnPush=move.isDoublePawnPush)

		newBoard.PlayMove(newMove) # This play move function does not need to check the legal moves 
								# because it will be checked outside of the function. 
								# Just update everything like usual assuming everything is correct.

		if KingChecked(newBoard, move.piece.color):
			del newBoard, newMove
			continue
		else:
			fullLegalMoves.append(move)
			del newBoard, newMove
	
	return fullLegalMoves


def GetSlidingPieceLegalMoves(board: Board, piece: Piece) -> list[Move]:
	LegalMoves = []

	for direction in piece.Directions: # Loop through all directions
		index = BoardPosToIndex(piece.board_pos)

		for i in range(GetNumberOfSquaresToEdge(piece.board_pos, direction)+1): # Step in each direction
			if i == 0: # Skip ourselves
				continue
				
			index += piece.IndexDirections[direction]

			if board.board[index] == '_': # If the square is blank, it is a legal move
				LegalMoves.append(Move(piece.board_pos, IndexToBoardPos(index), piece))
				continue

			elif board.board[index].color == piece.color: # If we run into our own piece, switch to another direction
				break
			
			else: # This is just if the piece is an enemy piece, we can capture, but cant go further
				LegalMoves.append(Move(piece.board_pos, IndexToBoardPos(index), piece))
				break

	return LegalMoves



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

def KingChecked(board: Board, color: str): # Returns whether or not the king of the color given is in check

	all_attacked_squares = []

	for piece in board.GetPieces(OppositeColor(color)): # Loop through all enemy pieces
		for square in piece.GetAttackedSquares(board):
			all_attacked_squares.append(square) # Add the squares that are attacked to the list
	
	if board.GetPiece(King, 'White').board_pos in all_attacked_squares:
		return True
	else:
		return False


def OppositeColor(color: str):
	if color == 'White': return 'Black'
	else: return 'White'

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

def DrawPieces(board: Board, DrawClickedPiece = True) -> None:
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

def DrawLegalMoves(piece: Piece, board: Board):
	LegalMoves = GenerateLegalMoves(board, piece)

	for move in LegalMoves:
		pygame.draw.rect(window, LegalMoveColor, pygame.Rect((move.target_square[0]*square_width, move.target_square[1]*square_height), square_size))



def ChangePlayColor(board: Board):
	if board.color == 'White': board.color = 'Black'
	else: board.color = 'White'

def Update():
	pygame.display.update()

window_size = (400, 400)
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
LegalMoveColor = (255, 153, 0)


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
					result = currentBoard.BoardMove(Move(start_square, target_square, clickedPiece))

					if result == "No Legal Moves":
						clickedPiece.SetBoardPos(start_square)
				
				else:
					clickedPiece.SetBoardPos(start_square)
			
			clickedPiece = None
			
		elif event.type == pygame.MOUSEMOTION:
			if mouseDown and clickedPiece != None:
				clickedPiece.rect.center = pygame.mouse.get_pos()
	
	window.fill('black')
	
	currentBoard.Draw()

	if clickedPiece:
		DrawLegalMoves(clickedPiece, currentBoard)

	
	DrawPieces(currentBoard)
	
	Update()