from typing import Optional, List, Tuple
from enum import Enum
from copy import deepcopy

from tile import Tile
from move import Move, Direction
from board_pos import Pos

class SquareType(Enum):
    Plain = 0
    LetterX2 = 1
    LetterX3 = 2
    WordX2 = 3
    WordX3 = 4

class Board:
    def __init__(self):
        self._board: List[List[Optional[Tile]]] = [[None] * 15 for _ in range(15)]
        self._moves: List[Move] = []
        self._move_scores: List[int] = []

    def get_tile(self, pos: Pos) -> Optional[Tile]:
        return self._board[pos.row][pos.col]

    def apply_move(self, move: Move) -> bool:
        """
        Applies the specified move to the board. Returns true if move was applied successfully, false if move was invalid (application did not take place)
        """
        if not (move.is_valid and self._has_anchor(move) and self._is_continuous(move)):
            return False

        for (tile, pos) in move:
            self._place_tile(tile, pos)
        
        self._move_scores.append(self._get_score(move))
        self._moves.append(move)
        return True
    
    def get_score(self, n: int = -1):
        """
        Returns the score of the n-th move (latest by default)
        """
        return self._move_scores[n]
    
    def undo_move(self, n: int = -1) -> int:
        """
        Undoes the n-th move (by default latest), and returns the score of the move
        """
        score = self._moves[n][1]
        del self._moves[n]
        return score
    
    def __iter__(self):
        return iter(self._board)

    def _place_tile(self, tile: Tile, pos: Pos):
        if self.get_tile(pos) is not None:
            raise ValueError(f"Tried to place tile on non-empty board position {pos}")
        self._board[pos.row][pos.col] = tile

    def _remove_tile(self, pos: Pos):
        if self.get_tile(pos) is None:
            raise ValueError(f"Tried to remove tile from empty board position {pos}")
        self._board[pos.row][pos.col] = None

    def _has_anchor(self, move: Move):
        """
        Checks that a move is touching an existing letter (or is going through the center square), and that all tiles are adjacent to another tile
        """
        for _, pos in move:
            if pos == Pos(7, 7): # Center tile
                return True
            
            if any(self.get_tile(adj) is not None for adj in pos.get_adjacent()):
                return True
            
        return False
    
    def _is_continuous(self, move: Move):
        """
        Checks that all tiles in a move are touching another tile, either already placed on the board or part of the move.
        """
        # O(n^2) but the length of a move is at most 7 so should be fine
        for _, pos in move:
            if all(self.get_tile(adj) is None and adj not in move.coordinates for adj in pos.get_adjacent()):
                return False
        return True

    def _get_score(self, move: Move):
        """
        Gets the score for the given move. Assumes the board state contains the tiles from the move.
        """
        assert all(tile == self.get_tile(pos) for tile, pos in move)

        def get_score_1D(placed_tiles: List[Pos], dir: Direction):
            score = 0
            word_multiplier = 1
            for tile, pos in self._get_tiles_through_pos(placed_tiles[0], dir):
                letter_multiplier = 1
                if pos in placed_tiles: # Only count multiplier if included in placed tiles
                    match Board._get_square_type(pos):
                        case SquareType.LetterX2:
                            letter_multiplier = 2
                        case SquareType.LetterX3:
                            letter_multiplier = 3
                        case SquareType.WordX2:
                            word_multiplier *= 2
                        case SquareType.WordX3:
                            word_multiplier *= 3
                
                score += letter_multiplier * tile.value
            
            return score * word_multiplier

        main_score = get_score_1D(move.coordinates, move.direction)
        bingo_bonus = 50 * (len(move.coordinates) == 7)
        cross_score = 0
        for pos in move.coordinates:
            cross_score += get_score_1D([pos], move.direction.opposite)

        return main_score + cross_score + bingo_bonus

    def _get_tiles_through_pos(self, anchor: Pos, dir: Direction):
        """
        Generates all tiles along the given direction going through the anchor position until an empty square or the board edge is reached
        """
        assert self.get_tile(anchor) is not None

        pos = anchor
        while pos.in_bounds and self.get_tile(pos) is not None:
            yield self.get_tile(pos), pos
            pos += dir.epsilon

        pos = anchor - dir.epsilon # Avoid double counting anchor
        while pos.in_bounds and self.get_tile(pos) is not None:
            yield self.get_tile(pos), pos
            pos -= dir.epsilon

    @staticmethod
    def _get_square_type(pos: Pos):
        """
        Returns the SquareType corresponding to a given board position.
        """
        # Exploit symmetry of board quadrants
        regularised_pos = deepcopy(pos).regularise()
        return Board._SQUARE_TYPES_TOP_LEFT[regularised_pos.row][regularised_pos.col]
    
    # Encodes the types of squares in Q4 of the board
    _SQUARE_TYPES_TOP_LEFT = [
        [SquareType.WordX3, SquareType.Plain, SquareType.Plain, SquareType.LetterX2, SquareType.Plain, SquareType.Plain, SquareType.Plain, SquareType.WordX3],
        [SquareType.Plain, SquareType.WordX2, SquareType.Plain, SquareType.Plain, SquareType.Plain, SquareType.LetterX3, SquareType.Plain, SquareType.Plain],
        [SquareType.Plain, SquareType.Plain, SquareType.WordX2, SquareType.Plain, SquareType.Plain, SquareType.Plain, SquareType.LetterX2, SquareType.Plain],
        [SquareType.LetterX2, SquareType.Plain, SquareType.Plain, SquareType.WordX2, SquareType.Plain, SquareType.Plain, SquareType.Plain, SquareType.LetterX2],
        [SquareType.Plain, SquareType.Plain, SquareType.Plain, SquareType.Plain, SquareType.WordX2, SquareType.Plain, SquareType.Plain, SquareType.Plain],
        [SquareType.Plain, SquareType.LetterX3, SquareType.Plain, SquareType.Plain, SquareType.Plain, SquareType.LetterX3, SquareType.Plain, SquareType.Plain],
        [SquareType.Plain, SquareType.Plain, SquareType.LetterX2, SquareType.Plain, SquareType.Plain, SquareType.Plain, SquareType.LetterX2, SquareType.Plain],
        [SquareType.WordX3, SquareType.Plain, SquareType.Plain, SquareType.LetterX2, SquareType.Plain, SquareType.Plain, SquareType.Plain, SquareType.WordX2]
    ]