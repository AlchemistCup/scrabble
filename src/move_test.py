import unittest

from tile import Tile
from board_pos import Pos
from move import Move
 
class TestIsValid(unittest.TestCase):
    def test_valid_vertical(self):
        move = Move([Tile('A'), Tile('B'), Tile('C')], [Pos(7, 7), Pos(7, 8), Pos(7, 9)])
        self.assert_(move.is_valid)

    def test_valid_horizontal(self):
        move = Move([Tile('A'), Tile('B'), Tile('C')], [Pos(7, 7), Pos(8, 7), Pos(9, 7)])
        self.assert_(move.is_valid)

    def test_invalid(self):
        move = Move([Tile('A'), Tile('B'), Tile('C')], [Pos(7, 7), Pos(8, 8), Pos(7, 9)])
        self.assertFalse(move.is_valid)

if __name__ == '__main__':
    unittest.main()