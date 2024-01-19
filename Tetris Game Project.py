# Eugenie Kim
# Tetris Game Project

import random, time, pygame, sys, os
from pygame.locals import *

# ----------PRE-GAME---------- #
# Pygame screen set up
pygame.init()

OBJWINDOW = pygame.display.set_mode((800,600))
pygame.display.set_caption('Tetris Clone')

# Fps clock controls
FPSCLOCK = pygame.time.Clock()
FPS = 120
FPSCOUNTDOWN = 120

# Font and image imports
BACKGROUND = pygame.transform.scale(pygame.image.load('TetrisBG.jpg'),(800,1000))

TITLEFONT = pygame.font.Font('ARCADE_I.ttf',80)
GENERALFONT = pygame.font.Font('Retro.ttf',20)

# Game constats
BOXSIZE = 20 
BOARDW = 10 
BOARDH = 20
XMARGIN = 300
YMARGIN = 150
BLANK = '.' 
PIECES = 'SZIOJLT'

# Game variables
iScore = 0
lBoard = []
lBlanks = [[],[]]
lRotBlanks = []

# Piece groups
ActiveBGroup = pygame.sprite.Group()
FrozenBGroup = pygame.sprite.Group()

# Detector groups
RDetectorsGroup = pygame.sprite.Group()
LDetectorsGroup = pygame.sprite.Group()
DDetectorsGroup = pygame.sprite.Group()

# Colours
WHITE = (255,255,255)
GRAY = (185,185,185)
BLACK = (0,0,0)

RED = (155,0,0)
LIGHTRED = (200,30,30)

GREEN = (0,155,0)
LIGHTGREEN = (30,200,30)

BLUE = (0,0,155)
LIGHTBLUE = (30,30,200)

YELLOW = (155,155,0)
LIGHTYELLOW = (200,200,30)

PURPLE = (155,0,155)
LIGHTPURPLE = (200,30,200)

AQUA = (0,155,155)
LIGHTAQUA = (30,200,200)

ORANGE = (200,100,0)
LIGHTORANGE = (255,155,30)

# Assigns colours to shapes
dCOLOURS = {'S':(RED,LIGHTRED),
			'Z':(GREEN,LIGHTGREEN),
			'I':(BLUE,LIGHTBLUE),
			'O':(YELLOW,LIGHTYELLOW),
			'J':(PURPLE,LIGHTPURPLE),
			'L':(AQUA,LIGHTAQUA),
			'T':(ORANGE,LIGHTORANGE)}

# ----------CLASSES---------- #
# cBrick(pieceX, pieceY, colours, x of block in piece, y of block in piece)
# creates and draws square on board, when brick hits bottom location added to lBoard
class cBrick (pygame.sprite.Sprite):
	def __init__(self,xLoc,yLoc,colours,x=0,y=0):
		# Pre: xLoc, yLoc must be integers and colours needs to be a tuple of two colours
		# Post: creates class attributes
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([BOXSIZE,BOXSIZE])
		self.rect = self.image.get_rect()
		self.rect.topleft = (xLoc + x)*BOXSIZE+XMARGIN+1,(yLoc + y)*BOXSIZE+YMARGIN+1
		self.loc = (xLoc + x), (yLoc + y)
		self.colours = colours

	def update(self,freeze):
		# Pre: freeze must be a boolean
		# Post: either marks the block on lBoard or draws the block onto the screen
		if freeze:
			lBoard[int(self.loc[1])+1] = lBoard[int(self.loc[1])+1][:int(self.loc[0])] + '1' +lBoard[int(self.loc[1])+1][int(self.loc[0])+1:]
			
		elif self.loc[1] >= 0:
			self.draw()
		
	def draw(self):
		# Pre: 
		# Post: draws a scquare with a lighter order
		pygame.draw.rect(OBJWINDOW, self.colours[0],(self.rect.x, self.rect.y, BOXSIZE-1, BOXSIZE-1),0)
		pygame.draw.rect(OBJWINDOW, self.colours[1],(self.rect.x, self.rect.y, BOXSIZE-1, BOXSIZE-1),2)

# cDetector((x,y in piece), (x,y on board),colour)
# creates invisible squares that are used to detect collisions of piece with frozen pieces
class cDetector (pygame.sprite.Sprite):
	def __init__(self,x,y,xLoc,yLoc):
		# Pre: x,y,xLoc,yLoc must all be integers
		# Post: class attributes assigned
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([BOXSIZE,BOXSIZE])
		self.rect = self.image.get_rect()
		self.rect.topleft = (xLoc + x)*BOXSIZE+XMARGIN+1,(yLoc + y)*BOXSIZE+YMARGIN+1
		self.loc = (xLoc + x), (yLoc + y)

# ----------FUNCTIONS---------- #
# Piece Creation
def spawnPiece():
	# Pre: 
	# Post: returns random shape
	
	shape = random.choice(PIECES)
	newPiece = {'shape':shape,
				'rotation': 0,
				'x': random.randint(0,5),
				'y': -4,
				'colours':dCOLOURS[shape]
				}
	return newPiece

def getShape(shape, position):
	# Pre: shape must be a string of one character from (SZOIJLT), position must be an integer
	# Post: returns the requested shape in its specified position
	
	# All shapes and their possible positions
	S = [[
		'......',
		'......',
		'......',
		'..dOOD',
		'.dOOX.',
		'..XX..'],
		
		[
		'......',
		'......',
		'.dOD..',
		'.dOOD.',
		'..XOD.',
		'...X..'],
		
		[
		'......',
		'......',
		'..dOOD',
		'.dOOX.',
		'..XX..',
		'......'],
		
		[
		'......',
		'......',
		'..dOD.',
		'..dOOD',
		'...XOD',
		'....X.']]

	Z = [[
		'......',
		'......',
		'......',
		'.dOOD.',
		'..XOOD',
		'...XX.'],
		
		[
		'......',
		'......',
		'..dOD.',
		'.dOOD.',
		'.dOX..',
		'..X...'],
		[
		'......',
		'......',
		'.dOOD.',
		'..XOOD',
		'...XX.',
		'......'],
		[
		'......',
		'......',
		'...dOD',
		'..dOOD',
		'..dOX.',
		'...X..']]

	I = [[
		'......',
		'.dOD..',
		'.dOD..',
		'.dOD..',
		'.dOD..',
		'..X...'],
		
		[
		'......',
		'......',
		'......',
		'......',
		'dOOOOD',
		'.XXXX.'],

		[
		'......',
		'..dOD.',
		'..dOD.',
		'..dOD.',
		'..dOD.',
		'...X..']]

	O = [[
		'......',
		'......',
		'......',
		'.dOOD.',
		'.dOOD.',
		'..XX..']]

	J = [[
		'......',
		'......',
		'..dOD.',
		'..dOD.',
		'.dOOD.',
		'..XX..'],
		
		[
		'......',
		'......',
		'.dOD..',
		'.dOOOD',
		'..XXX.',
		'......'],
		
		[
		'......',
		'......',
		'..dOOD',
		'..dOX.',
		'..dOD.',
		'...X..'],
		
		[
		'......',
		'......',
		'......',
		'.dOOOD',
		'..XXOD',
		'....X.']]

	L = [[
		'......',
		'......',
		'..dOD.',
		'..dOD.',
		'..dOOD',
		'...XX.'],

		[
		'......',
		'......',
		'......',
		'.dOOOD',
		'.dOXX.',
		'..X...'],

		[
		'......',
		'......',
		'.dOOD.',
		'..XOD.',
		'..dOD.',
		'...X..'],
		
		[
		'......',
		'......',
		'...dOD',
		'.dOOOD',
		'..XXX.',
		'......']]

	T = [[
		'......',
		'......',
		'......',
		'.dOOOD',
		'..XOX.',
		'...X..'],
		
		[
		'......',
		'......',
		'...dOD',
		'..dOOD',
		'...XOD',
		'....X.'],
		
		[
		'......',
		'......',
		'..dOD.',
		'.dOOOD',
		'..XXX.',
		'......'],
		
		[
		'......',
		'......',
		'..dOD.',
		'..dOOD',
		'..dOX.',
		'...X..']]
	
	# dictionary to match piece name to piece list
	dPIECES = {'S':S, 'Z':Z, 'I':I, 'O':O, 'J':J,'L':L, 'T':T}
	
	return(dPIECES[shape][position%len(dPIECES[shape])])

def rotationControl(piece):
	# Pre: piece must be a dictionary created from spawnPiece()
	# Post: counts blanks on side of piece if rotation happens
	# used to keep the piece inside the board during rotations
	
	# runs through rotated version of active piece
	shapeToDraw = getShape(piece['shape'],piece['rotation']+1) 
	xLoc, yLoc = piece['x'],piece['y']
	
	# records blanks in rotated piece into lRotBlanks
	lRotBlanks.clear()
	for x in range(6):
		for y in range(6):
			if shapeToDraw[y][x] != BLANK:
				lRotBlanks.append(x)

# Object Creation (visible piece bricks and detectors)
def createBricks(piece):
	# Pre: piece must be a dictionary created from spawnPiece()
	# Post: creates displayed piece bricks and active detectors
	
	# Gathers piece details from piece
	shapeToDraw = getShape(piece['shape'],piece['rotation'])
	colours = piece['colours']
	xLoc, yLoc = piece['x'],piece['y']
	
	# records how many blanks are in piece
	lBlanks[0].clear() # side blanks
	lBlanks[1].clear() # bottom blanks
	
	# empties groups of previous iterations of bricks/detectors (prevents lag)
	ActiveBGroup.empty()
	RDetectorsGroup.empty()
	LDetectorsGroup.empty()
	DDetectorsGroup.empty()
	
	# records blanks and creates bricks and objects of piece
	for x in range(6):
		for y in range(6):
			if shapeToDraw[y][x] == 'O':
				lBlanks[0].append(x)
				lBlanks[1].append(y)
				ActiveBGroup.add(cBrick(xLoc,yLoc,colours,x,y))
				
			elif shapeToDraw[y][x] == 'X':
				DDetectorsGroup.add(cDetector(x,y,xLoc,yLoc))
				
			elif shapeToDraw[y][x] == 'D':
				RDetectorsGroup.add(cDetector(x,y,xLoc,yLoc))
				
			elif shapeToDraw[y][x] == 'd':
				LDetectorsGroup.add(cDetector(x,y,xLoc,yLoc))

def createFrozenPieces():
	# Pre: lBoard must be made up of 21 strings of 10 characters
	# Post: All frozen pieces are created
	
	FrozenBGroup.empty() # prevents lag
	
	# reads board to create all frozen pieces
	for y in range(1,21):
		for x in range(10):
			if lBoard[y][x] == '1':
				FrozenBGroup.add(cBrick(x,y-1,(GRAY,WHITE)))

# Display Controls
def drawScore(score,x,y):
	# Pre: score must be a string, x and y must be integers, GENERALFONT must be defined
	# Post: displays and labels score of active game
	
	# score value
	ScoreNumDisplay = GENERALFONT.render(score, True, (255,255,255))
	OBJWINDOW.blit(ScoreNumDisplay,(x,y))
	
	# score label
	ScoreTextDisplay = GENERALFONT.render("Score:", True, (255,255,255))
	OBJWINDOW.blit(ScoreTextDisplay,(x,y-20))

def drawTitle():
	# Pre: TITLEFONT must be defined
	# Post: displays title on screen
	
	TitleDisplay = TITLEFONT.render("XTetris", True, (255,255,255))
	OBJWINDOW.blit(TitleDisplay,(800/2 - (len("XTetris")*38),15))

def drawNextPiece(piece):
	# Pre: piece must be created by spawnPiece(), GENERALFONT must be defined
	# Post: draws and labels the next piece in the game
	
	# next piece label
	NextPDisplay = GENERALFONT.render("Next Piece", True, (255,255,255))
	OBJWINDOW.blit(NextPDisplay,(100,280))
	
	# gather info from piece
	shapeToDraw = getShape(piece['shape'],piece['rotation'])
	colour = piece['colours']
	xLoc, yLoc = 100,300
	
	# draw each of the boxes that make up the piece
	for x in range(6):
		for y in range(6):
			if shapeToDraw[x][y] == 'O':
				pygame.draw.rect(OBJWINDOW, colour[0], (xLoc + x*BOXSIZE, yLoc + y*BOXSIZE, BOXSIZE, BOXSIZE), 0)
				pygame.draw.rect(OBJWINDOW, colour[1], (xLoc + x*BOXSIZE, yLoc + y*BOXSIZE, BOXSIZE, BOXSIZE), 3)

def drawHoldPiece(piece):
	# Pre: piece must be created by spawnPiece(), GENERALFONT must be defined
	# Post: draws and labels the piece being held
	
	# hold piece label
	NextPDisplay = GENERALFONT.render("Hold:", True, (255,255,255))
	OBJWINDOW.blit(NextPDisplay,(100,120))
	
	# only draws the hold piece if there is one
	if piece != None:
		shapeToDraw = getShape(piece['shape'],piece['rotation'])
		colour = piece['colours']
		xLoc, yLoc = 100,140
		
		# draw each of the boxes that make up the piece
		for x in range(6):
			for y in range(6):
				if shapeToDraw[x][y] == 'O':
					pygame.draw.rect(OBJWINDOW, colour[0], (xLoc + x*BOXSIZE, yLoc + y*BOXSIZE, BOXSIZE, BOXSIZE), 0)
					pygame.draw.rect(OBJWINDOW, colour[1], (xLoc + x*BOXSIZE, yLoc + y*BOXSIZE, BOXSIZE, BOXSIZE), 3)

def drawBoard(score):
	# Pre: score must be a string
	#drawScore, drawTitle, drawNextPiece, drawHoldPiece, drawFrozenPiece functions must exist
	# Post: draws the board and all the text and pieces
	
	# draw none game related displays (background, title, score, next piece, hold piece)
	OBJWINDOW.blit(BACKGROUND,(0,0)) 
	drawScore(score,100,500)
	drawTitle()
	drawNextPiece(NextPiece)
	drawHoldPiece(HoldPiece)
	
	# draws board lines and rectangle
	pygame.draw.rect(OBJWINDOW, BLACK,(XMARGIN,YMARGIN,BOARDW*BOXSIZE,BOARDH*BOXSIZE),0)
	for hor in range(BOARDH+1):
		pygame.draw.line(OBJWINDOW, WHITE, (XMARGIN,YMARGIN+hor*BOXSIZE),(XMARGIN+BOARDW*BOXSIZE,YMARGIN+hor*BOXSIZE),1)
		
	for ver in range(BOARDW+1):
		pygame.draw.line(OBJWINDOW, WHITE, (XMARGIN+ver*BOXSIZE,YMARGIN),(XMARGIN+ver*BOXSIZE,YMARGIN+BOARDH*BOXSIZE),1)

	
	# draws active piece and frozen bricks
	createFrozenPieces()
	FrozenBGroup.update(False)
	
	ActiveBGroup.update(False)

def drawHighScores():
	# Pre: TetrisScores text file must exist, GENERALFONT must be defined
	# Post: finds and displays the highest score out of all scores on textfile
	
	# creates record of past scores from text file
	PastScores = open('TetrisScores.txt','r')
	lScores = []
	for line in PastScores.readlines():
		lScores.append(int(line))
	
	# highscore label
	HighScoresTextDisplay = GENERALFONT.render("High Scores:", True, (255,255,255))
	OBJWINDOW.blit(HighScoresTextDisplay,(40,200))
	
	# highscore value
	HighScoreNumDisplay = GENERALFONT.render(str(max(lScores)), True, (255,255,255))
	OBJWINDOW.blit(HighScoreNumDisplay,(40,220))

def drawGameOver(score):
	# Pre: TITLEFONT,GENERALFONT must be defined, drawScore() and drawHighScores() functions must exist
	# Post: draws end screen
	
	OBJWINDOW.fill(BLACK)
	
	# game over title
	gameOverDisplay = TITLEFONT.render("GAME OVER", True, (255,0,0))
	OBJWINDOW.blit(gameOverDisplay,(800/2-(len("GAME OVER")*39),30))
	
	# restart instructions
	restartDisplay = GENERALFONT.render("Press ENTER to play again",True,(255,255,255))
	OBJWINDOW.blit(restartDisplay,(1,570))
	
	# displays current score and highscore
	drawScore(score,40,350)
	drawHighScores()

# Game Controlling
def clearLines():
	# Pre: lBoard must be made up of 21 strings of 10 characters
	# Post: clears full rows of frozen pieces and adds 100 for each row
	# doubles whole score for a tetris (4 rows in one piece)
	
	iScored = 0
	
	# parses through board
	for line in range(1,21):
		# finds and clears full lines
		if lBoard[line] == '1'*10:
			lBoard.pop(line)
			lBoard.insert(0,'0'*10)
			
			iScored += 1 # records how many lines are clear
	
	# doubles scored points for tetris
	if iScored == 4: 
		iScored *= 2
	
	return 100*iScored

def lossCheck():
	# Pre: lBoard must be a defined list, saveScore() function must exist
	# Post: If there are any blocks outside of the top of the board game ends
	#and score is added to a textfile with previous scores
	
	# checks for frozen piece on top of board (first row of lBoard isn't part of board)
	if '1' in lBoard[0]:
		saveScore(str(iScore)+'\n')
		return False
	return True

def createBoard(board):
	# Pre: board must be a list
	# Post: creates empty board list
	board.clear()
	for _ in range(21):
		board.append('0000000000')

# Score Recording
def saveScore(score):
	# Pre: TextScores textfile must exist, score must be a string
	# Post: saves score to record of previous scores
	
	PastScores = open('TetrisScores.txt','a')
	PastScores.write(score)
	PastScores.close()

# ----------PIECE AND BOARD CREATION---------- #
ActivePiece = spawnPiece()
NextPiece = spawnPiece()
HoldPiece = None

createBricks(ActivePiece)
createBoard(lBoard)

# ----------GAME LOOPS AND ACTION CONTROLS---------- #
TuckOpportunity = False

Spaced = False
Hold = False

RunGame = True
Playing = True

# ----------GAME LOOP---------- #
while RunGame:
	
	# ----------TETRIS GAME---------- #
	while Playing:
		# check for loss and full lines
		Playing = lossCheck()
		iScore += clearLines()
		
		
		drawBoard(str(iScore))
		
		
		# ----------EVENT PUMP---------- #
		for event in pygame.event.get():
			
			# Quit check
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			
			# Keyboard checks
			if event.type == pygame.KEYDOWN:
				
				# checking if detectors collide with frozen pieces
				RdetectorCollisions = list(pygame.sprite.groupcollide(RDetectorsGroup,FrozenBGroup,False,False,collided=None))
				LdetectorCollisions = list(pygame.sprite.groupcollide(LDetectorsGroup,FrozenBGroup,False,False,collided=None))
				DdetectorCollisions = list(pygame.sprite.groupcollide(DDetectorsGroup,FrozenBGroup,False,False,collided=None))
				
				# Quick drop
				if event.key == pygame.K_SPACE: 
					Spaced = True
				
				# Movements
				elif event.key == pygame.K_RIGHT and ActivePiece['x'] < BOARDW-6+5-max(lBlanks[0]) and RdetectorCollisions == []:
					ActivePiece['x'] += 1
				elif event.key == pygame.K_LEFT and ActivePiece['x'] > 0-min(lBlanks[0]) and LdetectorCollisions == []:
					ActivePiece['x'] -= 1
				elif event.key == pygame.K_DOWN and DdetectorCollisions == []:
					ActivePiece['y'] += 1
					iScore += 1
				
				# Rotation
				elif event.key == pygame.K_UP:
					
					# keeps piece inside board during rotations
					rotationControl(ActivePiece)
					if ActivePiece['x'] < 0-min(lRotBlanks):
						ActivePiece['x']= 0-min(lRotBlanks)
					elif ActivePiece['x'] > BOARDW-1-max(lRotBlanks):
						ActivePiece['x'] = BOARDW-1-max(lRotBlanks)
					
					ActivePiece['rotation'] += 1
				
				# Holds a piece
				elif event.key == pygame.K_c and not Hold: 
					Hold = True
					
					
					if HoldPiece == None: # Needed when there is no piece being held (start of game)
						HoldPiece = ActivePiece
						ActivePiece = NextPiece
						NextPiece = spawnPiece()
					
					else: 
						HoldPiece,ActivePiece = ActivePiece,HoldPiece
						
					# Brings held piece back to top
					HoldPiece['y'] = -2
		
		# creates Active piece bricks
		createBricks(ActivePiece) 
		
		# checks if piece is at bottom or hitting frozen pieces
		collisions = list(pygame.sprite.groupcollide(DDetectorsGroup,FrozenBGroup,False,False,collided=None))
		if ActivePiece['y'] == 19-max(lBlanks[1]) or collisions != []:
			if not TuckOpportunity: # gives small time space to tuck pieces
				BreathTime = time.time()
				TuckOpportunity = True
			
			if Spaced or time.time() >= BreathTime + .3: 
				# Sets up new Active piece and next piece
				ActivePiece = NextPiece
				NextPiece = spawnPiece()
				
				ActiveBGroup.update(True) # adds now frozen piece bricks onto lBoard
				
				# resets hold, quick drop and tuck chance
				Spaced = False
				TuckOpportunity = False
				Hold = False
				
		# carries piece to bottom if space used
		if Spaced:
			iScore += 1
			ActivePiece['y']+=1
		
		# has the pieces moving down screen at 1 FPS at start, speeding up overtime
		if FPSCOUNTDOWN < 0 and not TuckOpportunity:
			iScore += 1
			
			ActivePiece['y'] += 1
			
			FPS += .5 
			FPSCOUNTDOWN = 120
		FPSCOUNTDOWN -= 1
		
		# pygame management
		FPSCLOCK.tick(FPS)
		pygame.display.update()
	
	# ----------END SCREEN---------- #
	
	drawGameOver(str(iScore))
	
	# ----------EVENT PUMP---------- #
	for event in pygame.event.get():
		# Quit check
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		
		# Restart Game check
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				Playing = True
				createBoard(lBoard)
				iScore = 0
	
	# pygame management
	FPSCLOCK.tick(FPS)
	pygame.display.update()

