import unittest

from tile import Tile
from board_pos import Pos
from move import Move, Direction

class TestIsValid(unittest.TestCase):
    def test_valid_horizontal(self):
        move = Move([Tile('A'), Tile('B'), Tile('C')], [Pos(7, 7), Pos(7, 8), Pos(7, 9)])
        self.assert_(move.is_valid)
        self.assertEqual(move.direction, Direction.Horizontal)

    def test_valid_vertical(self):
        move = Move([Tile('E'), Tile('G'), Tile('G')], [Pos(7, 7), Pos(8, 7), Pos(9, 7)])
        self.assert_(move.is_valid)
        self.assertEqual(move.direction, Direction.Vertical)

    def test_valid_discontinuous(self):
        move = Move([Tile('E'), Tile('G'), Tile('G')], [Pos(4, 7), Pos(6, 7), Pos(9, 7)])
        self.assert_(move.is_valid)

    def test_invalid_alignment(self):
        move = Move([Tile('P'), Tile('U'), Tile('T')], [Pos(7, 7), Pos(8, 8), Pos(7, 9)])
        self.assertFalse(move.is_valid)

    def test_invalid_repeated_positions(self):
        move = Move([Tile('P'), Tile('U'), Tile('L'), Tile('L')], [Pos(7, 8), Pos(8, 8), Pos(8, 8), Pos(10, 8)])
        self.assertFalse(move.is_valid)

class TestFromString(unittest.TestCase):
    def test_valid_horizontal(self):
        expected = Move([Tile('A'), Tile('B'), Tile('C')], [Pos(7, 7), Pos(7, 8), Pos(7, 9)])
        move = Move.fromstr('8H ABC')
        self.assertEqual(move, expected)

    def test_valid_vertical(self):
        expected = Move([Tile('E'), Tile('G'), Tile('G')], [Pos(7, 7), Pos(8, 7), Pos(9, 7)])
        move = Move.fromstr('H8 EGG')
        self.assertEqual(move, expected)

    def test_valid_discontinuous(self):
        expected = Move([Tile('E'), Tile('G'), Tile('G')], [Pos(4, 7), Pos(6, 7), Pos(9, 7)])
        move = Move.fromstr('H5 E.G..G')
        self.assertEqual(move, expected)

class TestDirection(unittest.TestCase):
    def test_horizontal(self):
        move = Move([Tile('G'), Tile('A'), Tile('S'), Tile('S')], [Pos(3, 1), Pos(3, 2), Pos(3, 3), Pos(3, 5)])
        self.assertEqual(move.direction, Direction.Horizontal)

    def test_vertical(self):
        move = Move([Tile('T'), Tile('O')], [Pos(11, 2), Pos(12, 2)])
        self.assertEqual(move.direction, Direction.Vertical)

if __name__ == '__main__':
    unittest.main()