from typing import Optional, List, Tuple
from enum import Enum

from tile import Tile
from move import Pos, Move

class Board:
    def __init__(self):
        self._board: List[List[Optional[Tile]]] = [[None] * 15 for _ in range(15)]
        self._moves: List[Tuple[Move, int]] = []

    def get_tile(self, pos: Pos) -> Optional[Tile]:
        return self._board[pos.row][pos.col]

    def apply_move(self, move: Move) -> int:
        """
        Applies the specified move to the board, and returns its score. Throws if move is invalid.
        """
        assert move.is_valid
        assert self._has_anchor(move)

        for (tile, pos) in move:
            self._place_tile(tile, pos)
        
        score = self._get_score(move)
        self._moves.append(move, score)
        return score
    
    def undo_move(self, n: int = -1) -> int:
        """
        Undoes the n-th move (by default latest), and returns the score of the move
        """
        score = self._moves[n][1]
        del self._moves[n]
        return score

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
        Checks that a move is touching an existing letter (or is going through the center square)
        """
        for _, pos in move:
            if pos == Pos(7, 7): # Center tile
                return True
            
            if any(self.get_tile(adj) is not None for adj in pos.get_adjacent()):
                return True
            
        return False

    def _get_score(self, move: Move):
        start = move.start
        end = move.end

        bingo_bonus = 50 * (len(move) == 7)

        assert False, "Not yet implemented"

        # if move.is_horizontal:
        #     while start.row > 0 and self.get_tile(start) is not None:
        #         start -= Pos(1, 0)
        #     while end.row < 14 and self.get_tile(end) is not None:
        #         end +=
