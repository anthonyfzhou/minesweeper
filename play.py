from board import Board
import argparse

def main(n, num_mines):
    # TODO: Write commandline game
    gameContinue = True;

    if (num_mines > (n * n)):
    	print("Too many mines, please try again!")
    	return

    while gameContinue:
    	# Generate a new board
    	currBoard = Board(n, num_mines)
    	gameContinue = playGame(currBoard)

    # Game completed, exit the program
    print("Thanks for playing!")

def displayWin(board):
	board.displayBoard()
	print("Congratulations! You won!")

def displayLoss(board):
	for mine in board.minePositions:
		board.display[mine[0]][mine[1]] = "M"
	board.displayBoard()
	print("You lost this game :(")

def validate_int():
	while True:
		try:
			num = int(input())
		except ValueError:
			print("Please enter an integer!")
			continue
		else:
			return num

def validate_str():
	while True:
		try:
			response = str(input())
		except ValueError:
			print("Please enter a string")
			continue
		if response.lower() not in ('y', 'n'):
			print("Please select a valid option")
			continue
		else:
			return response.lower() == 'y'


def playGame(board):
	# While the game isn't completed, take turns sequentially
	while (not board.gameOver):

		board.displayBoard()
		# Parse user input

		# NEED TO VALIDATE INPUT
		print("Please enter the row number:")
		row = validate_int()

		print("Please enter the column number:")
		col = validate_int()

		board.takeMove(row, col)
		# board.gamestate = True

	if (board.gameWon):
		displayWin(board)
	else:
		displayLoss(board)

	# Game finished, prompt user to play again
	gameContinue = False
	print("Would you like to continue? (y/n):")
	# Validate input here also
	gameContinue = validate_str()

	return gameContinue

# DO NOT EDIT--------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', nargs='?', type=int, default=10)
    parser.add_argument('num_mines', nargs='?', type=int, default=10)
    return parser.parse_args() 

if __name__ == "__main__":
    args = parse_args()
    main(args.n, args.num_mines)

# DO NOT EDIT--------------------------------------------
