import unittest

from board_pos import Pos, Direction

class TestFromString(unittest.TestCase):
    def test_valid(self):
        pos_str = '6G'
        pos, dir = Pos.fromstr(pos_str)
        self.assertEqual(pos, Pos(5, 6))
        self.assertEqual(pos_str, pos.format(dir))
        self.assertEqual(dir, Direction.Horizontal)

        pos_str = 'G6'
        pos, dir = Pos.fromstr(pos_str)
        self.assertEqual(pos, Pos(5, 6))
        self.assertEqual(pos_str, pos.format(dir))
        self.assertEqual(dir, Direction.Vertical)


    def test_invalid_format(self):
        pos_str = '7_G'
        with self.assertRaises(ValueError):
            Pos.fromstr(pos_str)

    def test_out_of_bounds(self):
        row_oob = '16B'
        with self.assertRaises(ValueError):
            Pos.fromstr(row_oob)

        col_oob = '12P'
        with self.assertRaises(ValueError):
            Pos.fromstr(col_oob)

class TestGetAdjacent(unittest.TestCase):
    def test_center(self):
        pos = Pos(2, 3)
        adjacent_moves = list(pos.get_adjacent())
        self.assertCountEqual(adjacent_moves, [Pos(1, 3), Pos(3, 3), Pos(2, 2), Pos(2, 4)])

    def test_corner(self):
        pos = Pos(0, 0)
        adjacent_moves = list(pos.get_adjacent())
        self.assertCountEqual(adjacent_moves, [Pos(1, 0), Pos(0, 1)])

    def test_horizontal(self):
        pos = Pos(8, 9)
        adjacent_moves = list(pos.get_adjacent(Direction.Horizontal))
        self.assertCountEqual(adjacent_moves, [Pos(8, 8), Pos(8, 10)])

        pos = Pos(6, 14)
        adjacent_moves = list(pos.get_adjacent(Direction.Horizontal))
        self.assertCountEqual(adjacent_moves, [Pos(6, 13)])

    def test_vertical(self):
        pos = Pos(12, 5)
        adjacent_moves = list(pos.get_adjacent(Direction.Vertical))
        self.assertCountEqual(adjacent_moves, [Pos(11, 5), Pos(13, 5)])

        pos = Pos(14, 2)
        adjacent_moves = list(pos.get_adjacent(Direction.Vertical))
        self.assertCountEqual(adjacent_moves, [Pos(13, 2)])

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