import random
from queue import Queue

class Board:
    def __init__(self, n, num_mines):
    	self.n = n
    	self.num_mines = num_mines
    	self.revealedTiles = 0
    	self.board = []
    	self.display = []
    	self.minePositions = []
    	self.directions = [-1, 0, 1]
    	self.tilesNeeded = n * n - num_mines
    	self.gameWon = False

    	if (num_mines > (n * n)):
    		print("Too many mines!")
    		return None

    	for i in range(n):
    		self.display.append(["?"] * n)
    		self.board.append([0] * n)

    	self.generate_mines()

    	self.gameOver = False


    def displayBoard(self):
    	currRow = 0

    	# Printing column labels
    	print("    ", end ="")
    	for col in range(self.n):
    		print(col, end = "   ")
    	print("\n")
    	for row in self.display:
    		print(currRow, end = " | ")
    		for elem in row:
    			print(elem, end = "   ")
    		currRow+=1
    		print("\n")


    def generate_mines(self):
    	mines_placed = 0
    	while (mines_placed < self.num_mines):
    		position = random.randint(0, (self.n * self.n) - 1)
    		row = position // self.n
    		col = position % self.n
    		# check if mine already placed
    		if (self.board[row][col] != 1):
    			self.board[row][col] = 1
    			self.minePositions.append([row, col])
    			mines_placed += 1

    def isValid(self, row, col):
    	if (row < 0 or row >= self.n or col < 0 or col >= self.n):
    		return False
    	return True

    # Check if a tile is adjacent to a mine
    def adjacentMines(self, row, col):
    	mines = 0
    	for tile in self.getAdjacentTiles(row, col):
    		if (self.board[tile[0]][tile[1]] == 1):
    			mines += 1
    	return mines


    # Breadth-First search from starting square
    def BFS(self, row, col):
    	fringe = Queue()
    	fringe.put([row, col])
    	revealed = []

    	while (not fringe.empty()):
    		tile = fringe.get()
    		currRow = tile[0]
    		currCol = tile[1]
    		# Already visited
    		if (self.display[currRow][currCol] != "?"):
    			continue
    		else:
    			self.display[currRow][currCol] = self.adjacentMines(currRow, currCol)
    			# add all neightbors if this is a blank space
    			if (self.display[currRow][currCol] == 0):
    				for tile in self.getAdjacentTiles(currRow, currCol):
    					newRow = tile[0]
    					newCol = tile[1]
    					# add all neighbors not mines and not blank space
    					if (self.display[newRow][newCol] == "?" 
    						and self.board[newRow][newCol] != 1):
    						fringe.put([newRow, newCol])
    			revealed.append(currRow * 10 + currCol)
    			self.revealedTiles += 1
    	return revealed

    def getAdjacentTiles(self, row, col):
    	adjacentTiles = []
    	for x in self.directions:
    		for y in self.directions:
    			newRow = row + x
    			newCol = col + y
    			# add all valid adjacent tiles, so can't be same tile
    			if (self.isValid(newRow, newCol) and not (newCol == col and newRow == row)):
    				adjacentTiles.append([newRow, newCol])
    	return adjacentTiles


    def takeMove(self, row, col):

    	# print("move taken", row * 10 + col)

		# Out of bounds
    	if (not self.isValid(row, col)):
    		print("Error: Position out of bounds! \n")
    		return

		# Played already 	
    	if (self.display[row][col] != "?"):
    		print("Error: Already revealed! \n")
    		return

		# Click a mine
    	if (self.board[row][col] == 1):
    		# Need to reveal all mines
    		self.gameWon = False
    		self.gameOver = True
    		return []

		# Click a square adjacent to a mine
    	elif (self.adjacentMines(row, col) > 0):
    		self.revealedTiles += 1
    		self.display[row][col] = self.adjacentMines(row, col)
    		ret = [row * 10 + col]

		# Click an empty space
    	else:
    		ret = self.BFS(row, col)

    	# Game won
    	if (self.revealedTiles == self.tilesNeeded):
    		self.gameWon = True
    		self.gameOver = True

    	# self.displayBoard()

    	return ret






