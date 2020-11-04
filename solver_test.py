import unittest
import unittest.mock
import io
from solver import solve
from board import Board

# This is some starter code to test.
# You can delete this and test however you like.

class TestSolver(unittest.TestCase):

	@unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
	def assert_mines(self, expected_output, mock_stdout):
		board = Board(10, 101)
		self.assertEqual(mock_stdout.getvalue(), expected_output)

	# mines can't exceed size
	def test_mines(self):
		self.assert_mines("Too many mines!\n")


	# Always win on an empty board
	def test_board_win(self):
		board = Board(10, 0)
		board.takeMove(0, 0)
		self.assertEqual(True, board.gameWon)

	# Always lose on a full board
	def test_board_lose(self):
		board = Board(10, 100)
		board.takeMove(0, 0)
		self.assertEqual(False, board.gameWon)


if __name__ == "__main__":
    unittest.main()