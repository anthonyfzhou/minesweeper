# TODO: Takes a board and attempts to solve the board. 
# Return a boolean indicating if the board was successfully solved.
def solve(board) -> bool:

	move = [5, 5]

	mineAdjacent = {}
	possibleTiles = {}
	mines = {}
	safe = {}

	# Each tile represented by integer 0-100
	for i in range(100):
		possibleTiles[i] = 0

	while (not board.gameOver):

		# print("discovered mines:", mines)
		newTiles = board.takeMove(move[0], move[1])

		if (not board.gameOver):

			for newTile in newTiles:
				# Revealed square so we remove it from possible tiles
				if (newTile in possibleTiles):
					possibleTiles.pop(newTile)

				if (newTile in safe):
					safe.pop(newTile)

				# If the revealed tile is mine-adjacent, we want to keep track of it
				if (board.display[newTile // 10][newTile % 10] != 0):
					mineAdjacent[newTile] = 0

			# Can we deduce any mines or any guaranteed non-mine tiles?
			tilesUpdated = 1
			while tilesUpdated > 0:
				tilesUpdated = 0
				removedTiles = []
				for pos in mineAdjacent.keys():
					row = pos // 10
					col = pos % 10

					# Get all unknown neighbors
					unknown = getAdjacentUnknown(board, row, col, mines, safe)

					# If we know all the neighbors, we no longer need to consider the current square
					if (len(unknown) == 0):
						removedTiles.append(pos)

					else:
						# If we are neighbored to a mine, subtract that from our display value
						remainingMines = board.display[row][col] - numNeighboringMines(board, row, col, mines)

						# If remaining number is 0, all neighbors are safe
						if (remainingMines == 0):
							tilesUpdated += 1
							for safeTile in unknown:
								safe[safeTile] = 0
								if (safeTile in possibleTiles):
									possibleTiles.pop(safeTile)
						# ELSE, If remaining unknown == # on display, all neighbors are mines
						elif (len(unknown) == remainingMines):
							tilesUpdated += 1
							for mineTile in unknown:
								mines[mineTile] = 0
								if (mineTile in possibleTiles):
									possibleTiles.pop(mineTile)

				for removedTile in removedTiles:
					mineAdjacent.pop(removedTile)

			# If we have squares that are guaranteed safe, take those moves first
			if (len(safe) > 0):
				# print("safe tiles:", safe)
				nextPosition = safe.popitem()[0]
				move = [nextPosition // 10, nextPosition % 10]
				# print("next move is safe move:", move)

			else:
				# reset percentages
				for candidate in possibleTiles:
					possibleTiles[candidate] = 0

				for tile in mineAdjacent.keys():
					row = tile // 10
					col = tile % 10
					# if the tile is mine-adjacent, update percentages of adjacent tiles
					if (board.display[row][col] != 0):
						adjacentTiles = getAdjacentUnknown(board, row, col, mines, safe)
						remainingMines = board.display[row][col] - numNeighboringMines(board, row, col, mines)

						tilePercentage = remainingMines / len(adjacentTiles)
						for adj in adjacentTiles:
							# If we didn't remove this option previously, update percentage
							if (adj in possibleTiles):
								possibleTiles[adj] = possibleTiles.get(adj) + tilePercentage
				# print(possibleTiles)

				minPercent = 1000000
				for pos in possibleTiles.keys():
					if possibleTiles[pos] < minPercent:
						minPercent = possibleTiles[pos]
						move = [pos // 10, pos % 10]

				# print("next move is probability move:", move)

						

	return board.gameWon

# Return number of known neighboring mines
def numNeighboringMines(board, row, col, mines):
	ret = 0
	for minePos in mines.keys():
		mineRow = minePos // 10
		mineCol = minePos % 10
		if ((abs(row - mineRow) <= 1) and (abs(col - mineCol) <= 1)):
			ret += 1
	return ret

# Return all adjacent squares that are not confirmed to be mines/safe
def getAdjacentUnknown(board, row, col, mines, safe):
	ret = []
	adjacent = board.getAdjacentTiles(row, col)
	for tile in adjacent:
		index = tile[0] * 10 + tile[1]
		if (board.display[tile[0]][tile[1]] == "?"
			and index not in mines
			and index not in safe):
			ret.append(tile[0] * 10 + tile[1])
	return ret

# Return all unrevealed adjacent tiles
def getBlankAdjacent(board, row, col):
	ret = []
	adjacent = board.getAdjacentTiles(row, col)
	for tile in adjacent:
		if (board.display[tile[0]][tile[1]] == "?"):
			ret.append([tile[0], tile[1]])
	return ret




