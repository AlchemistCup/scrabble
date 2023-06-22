import unittest

from src.tile import Tile
 
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
        self.assertEqual(tile, Tile('?').set_letter('F'))

    def test_neq(self):
        tile = Tile('Z')
        self.assertNotEqual(tile, Tile('D'))

class TestFromString(unittest.TestCase):
    def test_regular_tile(self):
        tile = Tile.fromstr('B')
        self.assertEqual(tile, Tile('B'))

    def test_blank_tile(self):
        tile = Tile.fromstr('c')
        self.assertEqual(tile, Tile('?').set_letter('C'))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            Tile.fromstr('AB')
        
        with self.assertRaises(ValueError):
            Tile.fromstr('.')

if __name__ == '__main__':
    unittest.main()