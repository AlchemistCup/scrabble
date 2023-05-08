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
        move = Move([Tile('E'), Tile('G'), Tile('G')], [Pos(7, 8), Pos(8, 8), Pos(9, 8)])
        self.assert_(move.is_valid)

        self.assertFalse(board.apply_move(move))
        self.assertEqual(board._board, Board()._board)
        self.assertEqual(board._moves, [])

    def test_first_move(self):
        board = Board()
        move = Move([Tile('E'), Tile('G'), Tile('G')], [Pos(7, 7), Pos(8, 7), Pos(9, 7)])
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
        move1 = Move([Tile('E'), Tile('G'), Tile('G')], [Pos(7, 7), Pos(8, 7), Pos(9, 7)])
        self.assert_(move1.is_valid)
        self.assert_(board.apply_move(move1))

        move2 = Move([Tile('A'), Tile('F'), Tile('F'), Tile('E')], [Pos(9, 8), Pos(9, 9), Pos(9, 10), Pos(9, 11)])
        self.assert_(move1.is_valid)
        
        self.assert_(board.apply_move(move2))
        self.assertEqual([board.get_tile(pos) for pos in move1.coordinates], move1._tiles)
        self.assertEqual([board.get_tile(pos) for pos in move2.coordinates], move2._tiles)
        self.assertEqual(board._moves, [move1, move2])

    def test_discontinuous_move_with_anchor(self):
        board = Board()
        move1 = Move([Tile('E'), Tile('G'), Tile('G')], [Pos(7, 7), Pos(8, 7), Pos(9, 7)])
        self.assert_(move1.is_valid)
        self.assert_(board.apply_move(move1))

        move2 = Move([Tile('A'), Tile('F'), Tile('F'), Tile('E')], [Pos(9, 8), Pos(9, 9), Pos(9, 10), Pos(9, 12)])
        self.assert_(move1.is_valid)
        
        self.assertFalse(board.apply_move(move2))
        self.assertEqual([board.get_tile(pos) for pos in move1.coordinates], move1._tiles)
        self.assertEqual([board.get_tile(pos) for pos in move2.coordinates], [None] * len(move2._tiles))
        self.assertEqual(board._moves, [move1])

if __name__ == '__main__':
    unittest.main()