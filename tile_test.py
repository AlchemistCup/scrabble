import unittest

from tile import Tile
 
class TestInvalidTiles(unittest.TestCase):
    def test_lowercase_letter(self):
        tile = Tile('e')
        self.assertEqual(tile._letter, 'E')

    def test_invalid_letter(self):
        with self.assertRaises(ValueError):
            Tile('.')

    def test_invalid_blank_letter(self):
        tile = Tile('?')
        with self.assertRaises(ValueError):
            tile.set_letter('?')

class TestEq(unittest.TestCase):
    def test_eq(self):
        tile = Tile('A')
        self.assertEqual(tile, Tile('a'))

    def test_eq_blank(self):
        tile = Tile('?').set_letter('f')
        self.assertEqual(tile, Tile('?'))

    def test_neq(self):
        tile = Tile('Z')
        self.assertNotEqual(tile, Tile('D'))

if __name__ == '__main__':
    unittest.main()