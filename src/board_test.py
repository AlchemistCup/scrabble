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

    def test_discontinuous_move_with_all_tiles_adjacent(self):
        board = Board()
        move1 = Move([Tile('A'), Tile('B'), Tile('A'), Tile('N'), Tile('D'), Tile('O'), Tile('N')], [Pos(7, 7), Pos(7, 8), Pos(7, 9), Pos(7, 10), Pos(7, 11), Pos(7, 12), Pos(7, 13)])
        self.assert_(move1.is_valid)
        self.assert_(board.apply_move(move1))

        move2 = Move([Tile('T'), Tile('E')], [Pos(8, 7), Pos(9, 7)])
        self.assert_(move2.is_valid)
        self.assert_(board.apply_move(move2))

        move3 = Move([Tile('O'), Tile('O'), Tile('R')], [Pos(8, 11), Pos(9, 11), Pos(10, 11)])
        self.assert_(move3.is_valid)
        self.assert_(board.apply_move(move3))

        # Edge case: All tiles in move are touching another tile on the board (or in the move), but the move is invalid as it forms 2 separate words in the same direction of play
        move4 = Move([Tile('F'), Tile('D'), Tile('T')], [Pos(9, 6), Pos(9, 8), Pos(9, 10)])
        self.assert_(move4.is_valid)
        self.assertFalse(board.apply_move(move4))

        for move in [move1, move2, move3]:
            self.assertEqual([board.get_tile(pos) for pos in move.coordinates], move._tiles)
        
        self.assertEqual([board.get_tile(pos) for pos in move4.coordinates], [None] * len(move4._tiles))
        self.assertEqual(board._moves, [move1, move2, move3])

class TestGetScore(unittest.TestCase):
    def test_bingo(self):
        board = Board()
        move1 = Move([Tile('A'), Tile('B'), Tile('A'), Tile('N'), Tile('D'), Tile('O'), Tile('N')], [Pos(7, 7), Pos(7, 8), Pos(7, 9), Pos(7, 10), Pos(7, 11), Pos(7, 12), Pos(7, 13)])
        self.assert_(board.apply_move(move1))
        self.assertEqual(board.get_score(), 74)

    def test_qi(self):
        board = Board()
        move1 = Move([Tile('t'), Tile('o')], [Pos(7, 6), Pos(7, 7)])
        self.assert_(board.apply_move(move1))
        self.assertEqual(board.get_score(), 4)

        move2 = Move([Tile('T'), Tile('i'), Tile('l')], [Pos(4, 6), Pos(5, 6), Pos(6, 6)])
        self.assert_(board.apply_move(move2))
        self.assertEqual(board.get_score(), 5)

        move3 = Move([Tile('i'), Tile('l')], [Pos(6, 5), Pos(6, 7)])
        self.assert_(board.apply_move(move3))
        self.assertEqual(board.get_score(), 5)

        # Triple letter bonus used twice
        move4 = Move([Tile('Q')], [Pos(5, 5)])
        self.assert_(board.apply_move(move4))
        self.assertEqual(board.get_score(), 62)




if __name__ == '__main__':
    unittest.main()