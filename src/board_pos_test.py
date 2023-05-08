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

class TestRegularise(unittest.TestCase):
    def test_Q1(self):
        pos = Pos(6, 12)
        self.assertEqual(pos.regularise(), Pos(6, 2))

    def test_Q2(self):
        pos = Pos(10, 9)
        self.assertEqual(pos.regularise(), Pos(4, 5))

        pos = Pos(13, 13)
        self.assertEqual(pos.regularise(), Pos(1, 1))

    def test_Q3(self):
        pos = Pos(14, 7)
        self.assertEqual(pos.regularise(), Pos(0, 7))

    def test_Q4(self):
        pos = Pos(1, 3)
        self.assertEqual(pos.regularise(), Pos(1, 3))

        pos = Pos(6, 6)
        self.assertEqual(pos.regularise(), Pos(6, 6))

    def test_invalid(self):
        pos = Pos(15, 0)
        self.assertFalse(pos.in_bounds)
        with self.assertRaises(AssertionError):
            pos.regularise()

if __name__ == '__main__':
    unittest.main()