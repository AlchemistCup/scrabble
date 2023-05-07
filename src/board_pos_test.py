import unittest

from board_pos import Pos
 
class TestGetAdjacent(unittest.TestCase):
    def test_center_pos(self):
        pos = Pos(2, 3)
        adjacent_moves = list(pos.get_adjacent())
        self.assertCountEqual(adjacent_moves, [Pos(1, 3), Pos(3, 3), Pos(2, 2), Pos(2, 4)])

    def test_edge_pos(self):
        pos = Pos(0, 0)
        adjacent_moves = list(pos.get_adjacent())
        self.assertCountEqual(adjacent_moves, [Pos(1, 0), Pos(0, 1)])

if __name__ == '__main__':
    unittest.main()