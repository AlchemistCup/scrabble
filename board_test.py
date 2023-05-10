import unittest

from board import Board
from move import Move
from tile import Tile
from board_pos import Pos
 
class TestApplyMove(unittest.TestCase):
    def test_invalid_move(self):
        board = Board()
        move = Move([Tile('P'), Tile('U'), Tile('T')], [Pos(7, 7), Pos(8, 8), Pos(7, 9)])
        self.assertFalse(move.is_valid)

        self.assertFalse(board.apply_move(move))
        self.assertEqual(board._board, Board()._board)
        self.assertEqual(board._moves, [])

    def test_move_no_anchor(self):
        board = Board()
        move = Move.fromstr('I8 EGG')
        self.assert_(move.is_valid)

        self.assertFalse(board.apply_move(move))
        self.assertEqual(board._board, Board()._board)
        self.assertEqual(board._moves, [])

    def test_first_move(self):
        board = Board()
        move = Move.fromstr('H8 EGG')
        self.assert_(move.is_valid)

        self.assert_(board.apply_move(move))
        self.assertEqual([board.get_tile(pos) for pos in move.coordinates], move._tiles)
        for i, row in enumerate(board):
            for j, tile in enumerate(row):
                if Pos(i, j) not in move.coordinates:
                    self.assertEqual(tile, None)
        self.assertEqual(board._moves, [move])

    def test_move_with_anchor(self):
        board = Board()
        move1 = Move.fromstr('H8 EGG')
        self.assert_(move1.is_valid)
        self.assert_(board.apply_move(move1))

        move2 = Move.fromstr('10I AFFE')
        self.assert_(move1.is_valid)
        
        self.assert_(board.apply_move(move2))
        self.assertEqual([board.get_tile(pos) for pos in move1.coordinates], move1._tiles)
        self.assertEqual([board.get_tile(pos) for pos in move2.coordinates], move2._tiles)
        self.assertEqual(board._moves, [move1, move2])

    def test_discontinuous_move_with_anchor(self):
        board = Board()
        move1 = Move.fromstr('H8 EGG')
        self.assert_(move1.is_valid)
        self.assert_(board.apply_move(move1))

        move2 = Move.fromstr('10I AFF.E')
        self.assert_(move1.is_valid)
        
        self.assertFalse(board.apply_move(move2))
        self.assertEqual([board.get_tile(pos) for pos in move1.coordinates], move1._tiles)
        self.assertEqual([board.get_tile(pos) for pos in move2.coordinates], [None] * len(move2._tiles))
        self.assertEqual(board._moves, [move1])

    def test_discontinuous_move_with_all_tiles_adjacent(self):
        board = Board()
        move1 = Move.fromstr('8H ABANDON')
        self.assert_(move1.is_valid)
        self.assert_(board.apply_move(move1))

        move2 = Move.fromstr('H9 TE')
        self.assert_(move2.is_valid)
        self.assert_(board.apply_move(move2))

        move3 = Move.fromstr('L9 OOR')
        self.assert_(move3.is_valid)
        self.assert_(board.apply_move(move3))

        # Edge case: All tiles in move are touching another tile on the board (or in the move), but the move is invalid as it forms 2 separate words in the same direction of play
        move4 = Move.fromstr('10G F.D.T')
        self.assert_(move4.is_valid)
        self.assertFalse(board.apply_move(move4))

        for move in [move1, move2, move3]:
            self.assertEqual([board.get_tile(pos) for pos in move.coordinates], move._tiles)
        
        self.assertEqual([board.get_tile(pos) for pos in move4.coordinates], [None] * len(move4._tiles))
        self.assertEqual(board._moves, [move1, move2, move3])

class TestGetScore(unittest.TestCase):
    def test_bingo(self):
        board = Board()
        # Also tests stacking multipliers (2xWord with 2xLetter)
        move1 = Move.fromstr('8H ABANDON')
        self.assert_(board.apply_move(move1))
        self.assertEqual(board.get_score(), 74)

    def test_qi(self):
        board = Board()
        move1 = Move.fromstr('8G TO')
        self.assert_(board.apply_move(move1))
        self.assertEqual(board.get_score(), 4)

        move2 = Move.fromstr('G5 TIL.')
        self.assert_(board.apply_move(move2))
        self.assertEqual(board.get_score(), 5)

        move3 = Move.fromstr('7F I.L')
        self.assert_(board.apply_move(move3))
        self.assertEqual(board.get_score(), 5)

        # Triple letter bonus used twice
        move4 = Move.fromstr('6F Q')
        self.assert_(board.apply_move(move4))
        self.assertEqual(board.get_score(), 62)

    def test_blank(self):
        board = Board()
        move1 = Move.fromstr('8D QiNDARS')
        self.assert_(board.apply_move(move1))
        self.assertEqual(board.get_score(), 102)




if __name__ == '__main__':
    unittest.main()