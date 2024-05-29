import pygame
import copy

pygame.init()

class Piece:
	def __init__(self, FEN_Notation: str, color: str, img: pygame.Surface, board_pos: tuple):
		self.FEN = FEN_Notation
		self.color = color
		#self.img = img
		self.board_pos = board_pos

		self.rect = pygame.Rect((board_pos[0]*square_width, board_pos[1]*square_height), (square_width, square_height))
	
	def Draw(self):
		#window.blit(self.img, self.rect.topleft)

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

	
	def Move(self, new_board_pos: tuple):
		Board[GetBoardIndex(self.board_pos[0], self.board_pos[1])] = '_'

		self.board_pos = new_board_pos

		Board[GetBoardIndex(self.board_pos[0], self.board_pos[1])] = self

		self.rect = pygame.Rect((new_board_pos[0]*square_width, new_board_pos[1]*square_height), (square_width, square_height))
	
	def GetLegalMoves(self) -> tuple[list[tuple[int]], list[tuple[int]]]: # Returns a list of positions on the board that are legal
		pass


class King(Piece):
	def __init__(self, FEN_Notation: str, color: str, img: pygame.Surface, board_pos: tuple):
		super().__init__(FEN_Notation, color, img, board_pos)
	
	def GetLegalMoves(self) -> list[tuple]:
		LegalMoves = []

		directions = []
		
		X, Y = self.board_pos
		index = GetBoardIndexPos(self.board_pos)

		if X >= 1:
			directions.append(-1)
		if X <= 6:
			directions.append(+1)
		if Y >= 1:
			directions.append(-8)
		if Y <= 6:
			directions.append(+8)

		if X >= 1 and Y >= 1:
			directions.append(-9)
		if X >= 1 and Y <= 6:
			directions.append(+7)
		if X <= 6 and Y >= 1:
			directions.append(-7)
		if X <= 6 and Y <= 6:
			directions.append(+9)

		for direction in directions:
			piece = Board[index+direction]
			
			if piece == '_':
				LegalMoves.append(BoardIndexToPos(index+direction))
			
			elif piece.color != self.color:
				LegalMoves.append(BoardIndexToPos(index+direction))
			
			else:
				continue

		return LegalMoves, LegalMoves

class Queen(Piece):
	def __init__(self, FEN_Notation: str, color: str, img: pygame.Surface, board_pos: tuple):
		super().__init__(FEN_Notation, color, img, board_pos)
	
	def GetLegalMoves(self) -> list[tuple]:
		LegalMoves = []

		for direction in Directions:
			index = GetBoardIndex(self.board_pos[0], self.board_pos[1])
			# This code will not loop around the board because the GetSquaresToEdge function gives the exact number of squares to the edge. It doens't go past.
			for i in range(GetNumberOfSquaresToEdge(self.board_pos, direction)+1): #You need to add one because the GetNumberOfSquaresToEdge gives the number of squares to the edge without including the start square. This legal moves code starts on, but skips, the start_square, to ensure you go all the way to the edges, you need to add 1
				if i == 0: continue 						# Skip ourselves (the piece we are getting the moves for)

				index += IndexDirections[direction] # Go to the target square

				if Board[index] == '_': 						# If the square is blank, add it to the legal moves and continue
					LegalMoves.append(BoardIndexToPos(index))
					continue
				
				if Board[index].color == self.color: 			# If we run into one of our own pieces, break
					break

				else:										# Everything else (just if the square is occupied by an enemy piece)
					LegalMoves.append(BoardIndexToPos(index))
					break
		
		return LegalMoves, LegalMoves


class Rook(Piece):
	def __init__(self, FEN_Notation: str, color: str, img: pygame.Surface, board_pos: tuple):
		super().__init__(FEN_Notation, color, img, board_pos)
	
	def GetLegalMoves(self) -> list[tuple]:
		LegalMoves = []

		RookDirections = ['Up', 'Down', 'Left', 'Right']

		for direction in RookDirections:
			index = GetBoardIndex(self.board_pos[0], self.board_pos[1])

			# This code will not loop around the board because the GetSquaresToEdge function gives the exact number of squares to the edge. It doens't go past.
			for i in range(GetNumberOfSquaresToEdge(self.board_pos, direction)+1): #You need to add one because the GetNumberOfSquaresToEdge gives the number of squares to the edge without including the start square. This legal moves code starts on, but skips, the start_square, to ensure you go all the way to the edges, you need to add 1
				if i == 0: continue 						# Skip ourselves (the piece we are getting the moves for)

				index += IndexDirections[direction] # Go to the target square

				if Board[index] == '_': 						# If the square is blank, add it to the legal moves and continue
					LegalMoves.append(BoardIndexToPos(index))
					continue

				if Board[index].color == self.color: 			# If we run into one of our own pieces, break
					break

				else:										# Everything else (just if the square is occupied by an enemy piece)
					LegalMoves.append(BoardIndexToPos(index))
					break
		
		return LegalMoves, LegalMoves

class Knight(Piece):
	def __init__(self, FEN_Notation: str, color: str, img: pygame.Surface, board_pos: tuple):
		super().__init__(FEN_Notation, color, img, board_pos)

	def GetLegalMoves(self) -> list[tuple]:
		LegalMoves = []

		# Do a lot of If Statements to find out whether or not the square is out of the board

		'''
			## ##
		#	 # #    #
		###	 # #  ###

		###  # #  ###
		#    # #    #
		    ## ##
		'''

		X, Y = self.board_pos
		index = GetBoardIndex(X, Y)

		# Upper Moves

		if (X >= 2) and (Y >= 1):							#	#
			LegalMoves.append(BoardIndexToPos(index-10))	#	###
		
		if (X >= 1) and (Y >= 2):							#	##
			LegalMoves.append(BoardIndexToPos(index-17))	#	 #
															#	 #

		if (X <= 6) and (Y >= 2):							#	##
			LegalMoves.append(BoardIndexToPos(index-15))	#	#
															#	#
		
		if (X <= 5) and (Y >= 1):							#	  #
			LegalMoves.append(BoardIndexToPos(index-6))		#	###

		# Lower Moves
		
		if (X <= 5) and (Y <= 6):							#	###
			LegalMoves.append(BoardIndexToPos(index+10))	#	  #
		
		if (X <= 6) and (Y <= 5):							#	#
			LegalMoves.append(BoardIndexToPos(index+17))	#	#
															#	##
		
		if (X >= 1) and (Y <= 5):							#	 #
			LegalMoves.append(BoardIndexToPos(index+15))	#	 #
															#	##
		
		if (X >= 2) and (Y <= 6):							#	###
			LegalMoves.append(BoardIndexToPos(index+6))		#	#
		
		NotOwnPieces = []

		for move in LegalMoves:
			piece = Board[GetBoardIndex(move[0], move[1])]

			if piece == '_': NotOwnPieces.append(move)
			
			else:
				if piece.color == self.color: continue
				else: NotOwnPieces.append(move)


		return NotOwnPieces, NotOwnPieces


class Bishop(Piece):
	def __init__(self, FEN_Notation: str, color: str, img: pygame.Surface, board_pos: tuple):
		super().__init__(FEN_Notation, color, img, board_pos)
	
	def GetLegalMoves(self) -> list[tuple]:
		LegalMoves = []

		BishopDirections = ['Top Left', 'Top Right', 'Bottom Left', 'Bottom Right']

		for direction in BishopDirections:
			index = GetBoardIndex(self.board_pos[0], self.board_pos[1])
			# This code will not loop around the board because the GetSquaresToEdge function gives the exact number of squares to the edge. It doens't go past.

			for i in range(GetNumberOfSquaresToEdge(self.board_pos, direction)+1): #You need to add one because the GetNumberOfSquaresToEdge gives the number of squares to the edge without including the start square. This legal moves code starts on, but skips, the start_square, to ensure you go all the way to the edges, you need to add 1
				if i == 0: continue 							# Skip ourselves (the piece we are getting the moves for)

				index += IndexDirections[direction] 			# Go to the target square

				if Board[index] == '_': 						# If the square is blank, add it to the legal moves and continue
					LegalMoves.append(BoardIndexToPos(index))
					continue

				if Board[index].color == self.color: 			# If we run into one of our own pieces, break
					break

				else:											# Everything else (just if the square is occupied by an enemy piece)
					LegalMoves.append(BoardIndexToPos(index))
					break
		
		return LegalMoves, LegalMoves

class Pawn(Piece):
	def __init__(self, FEN_Notation: str, color: str, img: pygame.Surface, board_pos: tuple):
		super().__init__(FEN_Notation, color, img, board_pos)
		self.moved = False
	
	def GetLegalMoves(self) -> list[tuple]:
		LegalMoves = []
		Attacking = []

		X, Y = self.board_pos
		index = GetBoardIndex(X, Y)

		if self.color == 'White': # White Pawn Code
			if (self.moved == False) and (Board[index-16] == '_') and (Board[index-8] == '_'): # Double Pawn Push
				LegalMoves.append(BoardIndexToPos(index-16))
			
			if Board[index-8] == '_': # Single Pawn Push
				LegalMoves.append(BoardIndexToPos(index-8))

			if Board[index-7] != '_' and Board[index-7].color != self.color and self.board_pos[0] <= 6: # Right Capture. Make sure it doesn't wrap around the board
				LegalMoves.append(BoardIndexToPos(index-7))
			
			if Board[index-9] != '_' and Board[index-9].color != self.color and self.board_pos[0] >= 1: # Left Capture
				LegalMoves.append(BoardIndexToPos(index-9))
			
			# En Passant for white

			if Board[index+1] != '_' and Board[index+1].FEN == 'p' and Board[index-7] == '_': # Right En Passant. Make sure the square above the pawn to be captured is free
				if Board[index+1] in DoublePawnPushes:
					LegalMoves.append(BoardIndexToPos(index-7))
			
			if Board[index-1] != '_' and Board[index-1].FEN == 'p' and Board[index+9] == '_': # Left En Passant. Make sure the square above the pawn to be captured is free
				if Board[index-1] in DoublePawnPushes:
					LegalMoves.append(BoardIndexToPos(index-9))
			
			if self.board_pos[0] >= 1:
				Attacking.append(BoardIndexToPos(index-9))

			if self.board_pos[0] <= 6:
				Attacking.append(BoardIndexToPos(index-7))

			

		else: # Black Pawn Code
			if (self.moved == False) and (Board[index+16] == '_') and (Board[index+8] == '_'): # Double Pawn Push
				LegalMoves.append(BoardIndexToPos(index+16))
			
			if Board[index+8] == '_': # Single Pawn Push
				LegalMoves.append(BoardIndexToPos(index+8))
			
			if Board[index+7] != '_' and Board[index+7].color != self.color and self.board_pos[0] >= 1: # Left Capture
				LegalMoves.append(BoardIndexToPos(index+7))
			
			if Board[index+9] != '_' and Board[index+9].color != self.color  and self.board_pos[0] <= 6: # Right Capture
				LegalMoves.append(BoardIndexToPos(index+9))
			
			# En Passant for black

			if Board[index+1] != '_' and Board[index+1].FEN == 'P' and Board[index+9] == '_': # Right En Passant. Make sure the square below the pawn to be captured is free
				if Board[index+1] in DoublePawnPushes:
					LegalMoves.append(BoardIndexToPos(index+9))
			
			if Board[index-1] != '_' and Board[index-1].FEN == 'P' and Board[index-7] == '_': # Left En Passant. Make sure the square above the pawn to be captured is free
				if Board[index-1] in DoublePawnPushes:
					LegalMoves.append(BoardIndexToPos(index-7))
			
			if self.board_pos[0] >= 1:
				Attacking.append(BoardIndexToPos(index+7))

			if self.board_pos[0] <= 6:
				Attacking.append(BoardIndexToPos(index+9))


		return LegalMoves, Attacking


def DrawBoard():
	for i in range(board_width): #X 
		for j in range(board_height): #Y
			if ((i+j) % 2) == 0:
				color = white_square_color
			else:
				color = black_square_color
			
			pygame.draw.rect(window, color, pygame.Rect((i*square_width, j*square_height), (square_width, square_height)))

def GenerateBoard():
	return [Rook('r', 'Black', BlackRook, (0, 0)),
		 	Knight('n', 'Black', BlackKnight, (1, 0)),
			Bishop('b', 'Black', BlackBishop, (2, 0)),
			Queen('q', 'Black', BlackQueen, (3, 0)),
			King('k', 'Black', BlackKing, (4, 0)),
			Bishop('b', 'Black', BlackBishop, (5, 0)),
			Knight('n', 'Black', BlackKnight, (6, 0)),
			Rook('r', 'Black', BlackRook, (7, 0)),

		 	Pawn('p', 'Black', BlackPawn, (0, 1)),
			Pawn('p', 'Black', BlackPawn, (1, 1)),
			Pawn('p', 'Black', BlackPawn, (2, 1)),
			Pawn('p', 'Black', BlackPawn, (3, 1)),
			Pawn('p', 'Black', BlackPawn, (4, 1)),
			Pawn('p', 'Black', BlackPawn, (5, 1)),
			Pawn('p', 'Black', BlackPawn, (6, 1)),
			Pawn('p', 'Black', BlackPawn, (7, 1)),

			'_', '_', '_', '_', '_', '_', '_', '_',
			'_', '_', '_', '_', '_', '_', '_', '_',
			'_', '_', '_', '_', '_', '_', '_', '_',
			'_', '_', '_', '_', '_', '_', '_', '_',

			Pawn('P', 'White', WhitePawn, (0, 6)),
			Pawn('P', 'White', WhitePawn, (1, 6)),
			Pawn('P', 'White', WhitePawn, (2, 6)),
			Pawn('P', 'White', WhitePawn, (3, 6)),
			Pawn('P', 'White', WhitePawn, (4, 6)),
			Pawn('P', 'White', WhitePawn, (5, 6)),
			Pawn('P', 'White', WhitePawn, (6, 6)),
			Pawn('P', 'White', WhitePawn, (7, 6)),

			Rook('R', 'White', WhiteRook, (0, 7)),
		 	Knight('N', 'White', WhiteKnight, (1, 7)),
			Bishop('B', 'White', WhiteBishop, (2, 7)),
			Queen('Q', 'White', WhiteQueen, (3, 7)),
			King('K', 'White', WhiteKing, (4, 7)),
			Bishop('B', 'White', WhiteBishop, (5, 7)),
			Knight('N', 'White', WhiteKnight, (6, 7)),
			Rook('R', 'White', WhiteRook, (7, 7))]

def DrawPieces():
	i = 0
	j = 0

	for piece in Board:
		if piece == '_':
			pass
		
		elif piece != clickedPiece:
			piece.Draw()


		if i == 7:
			j += 1
			i = 0
		
		else:
			i += 1
	
	if (clickedPiece != None) and (clickedPiece != '_'):
		clickedPiece.Draw()
	
def DrawLegalSquares():
	global clickedPiece

	if (clickedPiece != None) and (clickedPiece != '_'):
		legal_moves, _ = clickedPiece.GetLegalMoves()

		if legal_moves != None:
			for square in legal_moves:
				pygame.draw.rect(window, legal_square_color, pygame.Rect((square[0]*square_width, square[1]*square_height), (square_width, square_height)))

def DrawAttackedSquares(color: str):
	attacked = GetAttackedSquares(color)

	for square in attacked:
		pygame.draw.rect(window, attacked_square_color, pygame.Rect((square[0]*square_width, square[1]*square_height), (square_width, square_height)))
	
def GetAttackedSquares(color: str) -> list[tuple[int]]:
	pieces = GetAllPieces(color)

	#AttackedSquares = {}
	AttackedSquares = []

	for piece in pieces:
		_, attacked = piece.GetLegalMoves()
		#AttackedSquares[piece] = (attacked, piece.board_pos)
		for square in attacked:
			AttackedSquares.append(square)
	
	return AttackedSquares

def GetChecked(color: str): # Return true or false whether the king is in check
	if color == 'White': attacked = GetAttackedSquares('Black')
	else: attacked = GetAttackedSquares('White')


	for piece in Board:
		if piece != '_':
			if piece.color == color and (piece.FEN == 'k' or piece.FEN =='K'):
				if piece.board_pos in attacked:
					return True
				else:
					return False
				

def Update():
	pygame.display.update()

def GetBoardIndex(rank: int, file: int):
	return rank + file*board_width

def GetBoardIndexPos(pos: tuple):
	return pos[0] + pos[1]*board_width

def BoardIndexToPos(index: int):
	X = index % board_width
	Y = index // board_width

	return (X, Y)

def GetBoardPos(pos: tuple): # This is to be used with window coords NOT board coords. Use IndexToPos instead for board coords
	rank = int(pos[0]//square_width)
	file = int(pos[1]//square_height)

	if (rank > 7) or (rank < 0):
		return None
	
	elif (file > 7) or (file < 0):
		return None

	else:
		return (rank, file)

def GetNumberOfSquaresToEdge(start_square: tuple, dir: str): # 8 Different directions: Up = -8, Down = +8, Left = -1, Right = +1, Top Right = -7, Top Left = -9, Bottom Right = +9, Bottom Left = +7
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

def SquareOnBoard(square: tuple):
	return (GetBoardIndex(square) > 0) and (GetBoardIndex(square) < board_width*board_height)

def MovePiece():
	global Board, DoublePawnPushes

	if clickedPiece != '_': # As long as the clicked piece is an actual piece
		target_square = GetBoardPos(pygame.mouse.get_pos()) # Get the Rank and File of the mouse location

		if (target_square != None) and (target_square != clickedPiece.board_pos): # If the target loc was not outside, move to the target square

			MovePieceSub(target_square)

				
		else: # If the rank or file was out of the board then move to the same location
			clickedPiece.Move(clickedPiece.board_pos)













def MovePieceSub(target_square: tuple[int]):
	global Board, DoublePawnPushes, clickedPiece

	legal_moves, attacked = clickedPiece.GetLegalMoves()																										# Get the legal moves of the clicked piece

	if legal_moves != None:																															# If it has legal moves

		if target_square in legal_moves:																								# Check if the square to be moved into is in the legal moves
			# Make a copy of the board,double pawn pushes, and clicked piece to keep track of en passant
			
			pawnlocations = []
			for pawn in DoublePawnPushes:
				pawnlocations.append(pawn.board_pos)

			oldBoard = copy.deepcopy(Board)
			oldDoublePawnPushes = []
			oldClickedPiece = copy.deepcopy(clickedPiece)


			original_square = clickedPiece.board_pos

			for loc in pawnlocations:
				oldDoublePawnPushes.append(oldBoard[GetBoardIndexPos(loc)])

			# Finish that 

			DoublePawnPushes.clear()

			# Add double pawn pushes to the DoublePawnPush list

			if clickedPiece.FEN == 'P' and clickedPiece.moved == False: 																			# If a white pawn just moved
				if GetBoardIndex(clickedPiece.board_pos[0], clickedPiece.board_pos[1])-16 == GetBoardIndex(target_square[0], target_square[1]): 	# If it was a double pawn push
					DoublePawnPushes.append(clickedPiece)																							# Add it to the double pawn pushes list

			if clickedPiece.FEN == 'p' and clickedPiece.moved == False: 																			# If a black pawn just moved
				if GetBoardIndex(clickedPiece.board_pos[0], clickedPiece.board_pos[1])+16 == GetBoardIndex(target_square[0], target_square[1]): 	# If it was a double pawn push
					DoublePawnPushes.append(clickedPiece)																							# Add it to the double pawn pushes list	

			# Remove the pawn being En Passanted 

			if clickedPiece.FEN == 'P':																												# If the piece is a white pawn
				if GetPieceBoardPos(target_square) == '_' and target_square[0] != clickedPiece.board_pos[0]:										# If the sqaure to move to is blank, and if its in a different column
					if target_square[0] > clickedPiece.board_pos[0]:																				# If the target square is on the right
						Board[GetBoardIndexPos(clickedPiece.board_pos)+1] = '_'																		# Remove the piece being En Passanted on the right
					
					if target_square[0] < clickedPiece.board_pos[0]:																				# If the target square is on the left
						Board[GetBoardIndexPos(clickedPiece.board_pos)-1] = '_'																		# Remove the piece being En Passanted on the left


			if clickedPiece.FEN == 'p':																												# If the piece is a black pawn
				if GetPieceBoardPos(target_square) == '_' and target_square[0] != clickedPiece.board_pos[0]:										# If the sqaure to move to is blank, and if its in a different column
					if target_square[0] > clickedPiece.board_pos[0]:																				# If the target square is on the right
						Board[GetBoardIndexPos(clickedPiece.board_pos)+1] = '_'																		# Remove the piece being En Passanted on the right
					if target_square[0] < clickedPiece.board_pos[0]:																				# If the target square is on the left
						Board[GetBoardIndexPos(clickedPiece.board_pos)-1] = '_'																		# Remove the piece being En Passanted on the left

			clickedPiece.Move(target_square)																										# Move the piece because it is a legal move																											# And change the color of play

				

			if (clickedPiece.FEN == 'P') or (clickedPiece.FEN == 'p'): 																				# If a pawn moved, set its moved value
				clickedPiece.moved = True

			if GetChecked(currentColor):																											# If the move makes the king get checked, reset everything
				Board = oldBoard
				DoublePawnPushes = oldDoublePawnPushes
				clickedPiece = oldClickedPiece
				clickedPiece.Move(original_square)
			
			else:
				ChangePlayerColor()
	
		else:
			clickedPiece.Move(clickedPiece.board_pos)					# If the target square is not in the legal moves, put it back to its start square
	
	else:																# If there are no legal moves
		print('No Legal Moves')											# Print "No Legal Moves"

		clickedPiece.Move(target_square)								# Move the piece to the target square anyway

		ChangePlayerColor()	



def isLegalCheck(Piece: Piece, target_square: tuple, Board: list):
	BoardCopy = copy.deepcopy(Board)
	PieceCopy = copy.deepcopy(Piece)

	







def TestMovePiece(Piece: Piece, target_square: tuple, Board: list):
	pass




def GetPieceBoardPos(pos: tuple):
	return Board[GetBoardIndex(pos[0], pos[1])]

def ChangePlayerColor():
	global currentColor

	if currentColor == 'White': currentColor = 'Black'
	
	else: currentColor = 'White'

def GetAllPieces(color: str) -> list[Piece]:
	pieces = []

	for piece in Board:
		if piece == '_':
			continue
		else:
			if piece.color == color:
				pieces.append(piece)

	return pieces

def Reset():
	global Board, clickedPiece, currentColor, DoublePawnPushes

	Board = GenerateBoard()
	clickedPiece = None
	currentColor = 'White'
	DoublePawnPushes.clear()

window_width = 800
window_height = 800
window_size = (window_width, window_height)
window_name = "Chess V1"

window = pygame.display.set_mode(window_size)
pygame.display.set_caption(window_name)

board_width = 8
board_height = 8

square_width = window_width/board_width
square_height = window_height/board_height

black_square_color = (181, 136, 58)
white_square_color = (237, 217, 183)
legal_square_color = (239, 153, 54)
attacked_square_color = (255, 0, 0)

Directions = ['Top Left', 'Up', 'Top Right', 'Right', 'Bottom Right', 'Down', 'Bottom Left', 'Left']
IndexDirections = {'Top Left':-9, 'Up':-8, 'Top Right':-7, 'Right':+1, 'Bottom Right':+9, 'Down':+8, 'Bottom Left':+7, 'Left':-1}

DoublePawnPushes = []

# Pieces

WhiteKing = pygame.transform.scale(pygame.image.load('whiteking.png'), (square_width, square_height))
BlackKing = pygame.transform.scale(pygame.image.load('blackking.png'), (square_width, square_height))

WhiteQueen = pygame.transform.scale(pygame.image.load('whitequeen.png'), (square_width, square_height))
BlackQueen = pygame.transform.scale(pygame.image.load('blackqueen.png'), (square_width, square_height))

WhiteKnight = pygame.transform.scale(pygame.image.load('whiteknight.png'), (square_width, square_height))
BlackKnight = pygame.transform.scale(pygame.image.load('blackknight.png'), (square_width, square_height))

WhiteBishop = pygame.transform.scale(pygame.image.load('whitebishop.png'), (square_width, square_height))
BlackBishop = pygame.transform.scale(pygame.image.load('blackbishop.png'), (square_width, square_height))

WhiteRook = pygame.transform.scale(pygame.image.load('whiterook.png'), (square_width, square_height))
BlackRook = pygame.transform.scale(pygame.image.load('blackrook.png'), (square_width, square_height))

WhitePawn = pygame.transform.scale(pygame.image.load('whitepawn.png'), (square_width, square_height))
BlackPawn = pygame.transform.scale(pygame.image.load('blackpawn.png'), (square_width, square_height))

Board = GenerateBoard()


currentColor = 'White'

DrawAttacked = False

mouseDown = False
clickedPiece: Piece | None = None

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()

		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouseDown = True

			start_square = GetBoardPos(pygame.mouse.get_pos())
			
			clickedPiece = Board[GetBoardIndex(start_square[0], start_square[1])] # Get the piece that was clicked

			if (clickedPiece != '_') and (clickedPiece != None): # If the clicked piece is not blank and not nothing
				if clickedPiece.color != currentColor: # If the clicked piece is not the current color, set the clicked piece to none
					clickedPiece = None
		
		elif event.type == pygame.MOUSEBUTTONUP:
			mouseDown = False # The mouse isn't down
			
			if clickedPiece != None:
				MovePiece()

				clickedPiece = None
		
		elif event.type == pygame.MOUSEMOTION:
			if mouseDown:
				if (clickedPiece != '_') and (clickedPiece != None):
					clickedPiece.rect.center = pygame.mouse.get_pos()
		
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				Reset()
			elif event.key == pygame.K_c:
				DrawAttacked = not DrawAttacked
	
	
	window.fill('black')

	DrawBoard()
	if DrawAttacked:
		DrawAttackedSquares(currentColor)
	DrawLegalSquares()
	DrawPieces()
	Update()