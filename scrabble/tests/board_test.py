import unittest

from src.board import Board
from src.move import Move
from src.tile import Tile
from src.board_pos import Pos
 
class TestApplyMove(unittest.TestCase):
    def test_invalid_move(self):
        board = Board()
        move = Move([Tile('P'), Tile('U'), Tile('T')], [Pos(7, 7), Pos(8, 8), Pos(7, 9)])
        self.assertFalse(move.is_valid)

        self.assertFalse(board.apply_move(move))
        self.assertEqual(board._board, Board()._board)
        self.assertEqual(list(board.moves()), [])

    def test_first_move_no_anchor(self):
        board = Board()
        move = Move.fromstr('I8 EGG')
        self.assertTrue(move.is_valid)

        self.assertFalse(board.apply_move(move))
        self.assertEqual(board._board, Board()._board)
        self.assertEqual(list(board.moves()), [])

    def test_first_move(self):
        board = Board()
        move = Move.fromstr('H8 EGG')
        self.assertTrue(move.is_valid)

        self.assertTrue(board.apply_move(move))
        self.assertEqual([board._get_tile(pos) for pos in move.coordinates], move._tiles)
        for i, row in enumerate(board):
            for j, tile in enumerate(row):
                if Pos(i, j) not in move.coordinates:
                    self.assertEqual(tile, None)
        self.assertEqual(list(board.moves()), [move])

    def test_move_no_anchor(self):
        board = Board()
        move1 = Move.fromstr('H8 EGG')
        move2 = Move.fromstr('10I .AFFE')

        self.assertTrue(board.apply_move(move1))
        self.assertFalse(board.apply_move(move2))
        self.assertEqual([board._get_tile(pos) for pos in move1.coordinates], move1._tiles)
        for i, row in enumerate(board):
            for j, tile in enumerate(row):
                if Pos(i, j) not in move1.coordinates:
                    self.assertEqual(tile, None)
        self.assertEqual(list(board.moves()), [move1])

    def test_move_with_anchor(self):
        board = Board()
        move1 = Move.fromstr('H8 EGG')
        move2 = Move.fromstr('10H .AFFE')

        for move in [move1, move2]:
            self.assertTrue(move.is_valid)
            self.assertTrue(board.apply_move(move))
        
        for move in [move1, move2]:
            self.assertEqual([board._get_tile(pos) for pos in move.coordinates], move._tiles)
        self.assertEqual(list(board.moves()), [move1, move2])

    def test_discontinuous_move_with_anchor(self):
        board = Board()
        move1 = Move.fromstr('H8 EGG')
        self.assertTrue(move1.is_valid)
        self.assertTrue(board.apply_move(move1))

        move2 = Move.fromstr('10I AFF.E')
        self.assertTrue(move2.is_valid)
        
        self.assertFalse(board.apply_move(move2))
        self.assertEqual([board._get_tile(pos) for pos in move1.coordinates], move1._tiles)
        self.assertEqual([board._get_tile(pos) for pos in move2.coordinates], [None] * len(move2._tiles))
        self.assertEqual(list(board.moves()), [move1])

    def test_discontinuous_move_with_all_tiles_adjacent(self):
        board = Board()
        move1 = Move.fromstr('8H ABANDON')
        move2 = Move.fromstr('H9 TE')
        move3 = Move.fromstr('L9 OOR')

        for move in [move1, move2, move3]:
            self.assertTrue(move.is_valid)
            self.assertTrue(board.apply_move(move))

        # Edge case: All tiles in move are touching another tile on the board (or in the move), but the move is invalid as it forms 2 separate words in the same direction of play
        move4 = Move.fromstr('10G F.D.T')
        self.assertTrue(move4.is_valid)
        self.assertFalse(board.apply_move(move4))

        for move in [move1, move2, move3]:
            self.assertEqual([board._get_tile(pos) for pos in move.coordinates], move._tiles)
        
        self.assertEqual([board._get_tile(pos) for pos in move4.coordinates], [None] * len(move4._tiles))
        self.assertEqual(list(board.moves()), [move1, move2, move3])

class TestGetScore(unittest.TestCase):
    def test_bingo(self):
        board = Board()
        # Also tests stacking multipliers (2xWord with 2xLetter)
        move1 = Move.fromstr('8H ABANDON')
        self.assertTrue(board.apply_move(move1))
        self.assertEqual(board.get_score(), 74)

    def test_repeated_premium(self):
        board = Board()
        move1 = Move.fromstr('8G TO')
        move2 = Move.fromstr('G5 TIL.')
        move3 = Move.fromstr('7F I.L')
        move4 = Move.fromstr('6F Q') # Triple letter bonus used twice

        expected_scores = [4, 5, 5, 62]
        for move, score in zip([move1, move2, move3, move4], expected_scores):
            self.assertTrue(board.apply_move(move))
            self.assertEqual(board.get_score(), score)

    def test_blank(self):
        board = Board()
        move1 = Move.fromstr('8D QiNDARS')
        self.assertTrue(board.apply_move(move1))
        self.assertEqual(board.get_score(), 102)

class TestGetChallengeWords(unittest.TestCase):
    def test_get_word_single(self):
        board = Board()
        move1 = Move.fromstr('8B ETAERIO')
        self.assertTrue(board.apply_move(move1))
        self.assertSetEqual(board.get_challenge_words(), set(['ETAERIO']))

    def test_get_word_multiple(self):
        board = Board()
        move1 = Move.fromstr('8E HORN')
        move2 = Move.fromstr('G6 FA.M')
        move3 = Move.fromstr('10E PASTE')
        move4 = Move.fromstr('9G .OB')

        expected_words = [set(['HORN']), set(['FARM']), set(['PASTE', 'FARMS']), set(['MOB', 'NOT', 'BE'])]
        for move, expected in zip([move1, move2, move3, move4], expected_words):
            self.assertTrue(board.apply_move(move))
            self.assertSetEqual(board.get_challenge_words(), expected)

    def test_repeated_words_counted_once(self):
        # In the case of challenges, a word is identified by its unique spelling
        board = Board()
        move1 = Move.fromstr('8G TO')
        move2 = Move.fromstr('G5 TIL.')
        move3 = Move.fromstr('7F I.L')
        move4 = Move.fromstr('6F Q') # QI formed twice

        expected_words = [set(['TO']), set(['TILT']), set(['ILL', 'LO']), set(['QI'])]
        for move, expected in zip([move1, move2, move3, move4], expected_words):
            self.assertTrue(board.apply_move(move))
            self.assertSetEqual(board.get_challenge_words(), expected)

    def test_word_with_blank(self):
        board = Board()
        move1 = Move.fromstr('8C AQUiVER')
        move2 = Move.fromstr('F8 .NSI?T')

        self.assertTrue(board.apply_move(move1))
        self.assertSetEqual(board.get_challenge_words(), set(['AQUIVER']))

        self.assertTrue(board.apply_move(move2))
        self.assertEqual(board.get_challenge_words(), None)
        self.assertTrue(board.set_blanks('s'))
        self.assertSetEqual(board.get_challenge_words(), set(['INSIST']))
            

if __name__ == '__main__':
    unittest.main()