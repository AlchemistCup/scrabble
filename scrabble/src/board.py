from typing import Optional, List, Set
from enum import Enum

from src.tile import Tile
from src.move import Move, Direction
from src.board_pos import Pos

class SquareType(Enum):
    Plain = 0
    LetterX2 = 1
    LetterX3 = 2
    WordX2 = 3
    WordX3 = 4

class MoveInfo:
    def __init__(self, move: Move, score: int):
        self._move = move
        self._score = score

    @property
    def move(self):
        return self._move
    
    @property
    def score(self):
        return self._score

class Board:
    DIM = Pos.MAX_SIZE
    def __init__(self):
        self._board: List[List[Optional[Tile]]] = [[None] * Board.DIM for _ in range(Board.DIM)]
        self._move_info: List[MoveInfo] = []

    def moves(self):
        """
        Generates all the moves that have been performed on the board in order
        """
        for m in self._move_info:
            yield m.move

    def apply_move(self, move: Move) -> bool:
        """
        Applies the specified move to the board. Returns true if move was applied successfully, false if move was invalid (application did not take place)
        """
        if not (move.is_valid and self._has_anchor(move) and self._is_continuous(move)):
            return False

        for (tile, pos) in move: # type: ignore
            self._place_tile(tile, pos)
        
        score = self._get_score(move)
        self._move_info.append(MoveInfo(move, score))
        return True
    
    def set_blanks(self, blanks: str) -> bool:
        """
        Sets the blank tiles for the last move specified by blanks in word order. Returns true if operation completed successfully, false otherwise.
        """
        move = self._move_info[-1].move
        return move.set_blanks(blanks)
        
    def get_score(self, n: int = -1):
        """
        Returns the score of the n-th move (latest by default)
        """
        return self._move_info[n].score
    
    def get_challenge_words(self) -> Optional[Set[str]]:
        """
        Returns the set of words formed by the latest move, or None if an error is encountered.
        """
        move = self._move_info[-1].move
        if move.n_of_unset_blanks > 0:
            return None
        
        return self._get_words_formed(move)
    
    def undo_move(self, n: int = -1) -> int:
        """
        Undoes the n-th move (by default latest), and returns the score of the move
        """
        score = self._move_info[n].score
        del self._move_info[n]
        return score
    
    def __iter__(self):
        return iter(self._board)
    
    def __repr__(self) -> str:
        row_sep = "+-" * Board.DIM + "+\n"
        res = row_sep
        for row in self:
            for tile in row:
                if tile is None:
                    tile = ' '
                res += f"|{tile.format()}"
            res += f"|\n{row_sep}" 
        
        return res
    
    def _get_tile(self, pos: Pos) -> Optional[Tile]:
        return self._board[pos.row][pos.col]

    def _place_tile(self, tile: Tile, pos: Pos):
        if self._get_tile(pos) is not None:
            raise ValueError(f"Tried to place tile on non-empty board position {pos}")
        self._board[pos.row][pos.col] = tile

    def _remove_tile(self, pos: Pos):
        if self._get_tile(pos) is None:
            raise ValueError(f"Tried to remove tile from empty board position {pos}")
        self._board[pos.row][pos.col] = None

    def _has_anchor(self, move: Move):
        """
        Checks that a move is touching an existing letter (or is going through the center square), and that all tiles are adjacent to another tile
        """
        for _, pos in move:
            if pos == Pos(7, 7): # Center tile
                return True
            
            if any(self._get_tile(adj) is not None for adj in pos.get_adjacent()):
                return True
            
        return False
    
    def _is_continuous(self, move: Move):
        """
        Checks that all tiles in a move form a continuous word
        """
        curr = move.start
        while curr != move.end:
            if not curr.in_bounds:
                return False

            if curr not in move.coordinates and self._get_tile(curr) is None:
                return False
            
            curr += move.direction.epsilon

        return True

    def _get_score(self, move: Move):
        """
        Gets the score for the given move. Assumes the board state contains the tiles from the move.
        """
        assert all(tile == self._get_tile(pos) for tile, pos in move)

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
            opposite = move.direction.opposite
            if self._forms_new_word(pos, opposite):
                cross_score += get_score_1D([pos], opposite)

        return main_score + cross_score + bingo_bonus
    
    def _get_words_formed(self, move: Move) -> Set[str]:
        """
        Gets all the words formed by a particular move. Assumes the board state contains the tiles from the move.
        """
        assert all(tile == self._get_tile(pos) for tile, pos in move)

        def get_word_1D(anchor: Pos, dir: Direction):
            word = ''
            for tile, _ in self._get_tiles_through_pos(anchor, dir):
                word += tile.format()
            return word.upper()
        
        words_formed = set([get_word_1D(move.start, move.direction)])
        for pos in move.coordinates:
            opposite = move.direction.opposite
            if self._forms_new_word(pos, opposite):
                words_formed.add(get_word_1D(pos, opposite))

        return words_formed

    def _forms_new_word(self, pos: Pos, dir: Direction):
        """
        Returns True if a word is formed from the given position along the direction specified, meaning that there is a neighbouring tile along the direction specified
        """
        return any(self._get_tile(adj) is not None for adj in pos.get_adjacent(dir))

    def _get_tiles_through_pos(self, anchor: Pos, dir: Direction):
        """
        Generates all tiles along the given direction going through the anchor position until an empty square or the board edge is reached in order (i.e. top to bottom or left to right).
        """
        assert self._get_tile(anchor) is not None

        def _get_prev_tiles_rec(pos: Pos):
            prev_pos = pos - dir.epsilon
            if not prev_pos.in_bounds or self._get_tile(prev_pos) is None:
                yield self._get_tile(pos), pos
            else:
                yield from _get_prev_tiles_rec(prev_pos)
                yield self._get_tile(pos), pos

        yield from _get_prev_tiles_rec(anchor)
        pos = anchor + dir.epsilon
        while pos.in_bounds and self._get_tile(pos) is not None:
            yield self._get_tile(pos), pos
            pos += dir.epsilon

    @staticmethod
    def _get_square_type(pos: Pos):
        """
        Returns the SquareType corresponding to a given board position.
        """
        # Exploit symmetry of board quadrants
        regularised_pos = pos.regularise()
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