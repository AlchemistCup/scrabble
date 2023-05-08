from enum import Enum
from typing import Optional

class Direction(Enum):
    Horizontal = 0
    Vertical = 1

    @property
    def opposite(self):
        match self:
            case Direction.Horizontal:
                return Direction.Vertical
            case Direction.Vertical:
                return Direction.Horizontal
            
    @property
    def epsilon(self):
        """
        Returns minimum displacement along the direction
        """
        match self:
            case Direction.Horizontal:
                return Pos(0, 1)
            case Direction.Vertical:
                return Pos(1, 0)

class Pos:
    MAX_SIZE = 15

    def __init__(self, row: int, col: int):
        self._row = row
        self._col = col

    @property
    def row(self):
        return self._row
    
    @property
    def col(self):
        return self._col
    
    @property
    def in_bounds(self):
        return Pos._in_bounds(self.row) and Pos._in_bounds(self.col)
    
    def get_adjacent(self, dir: Optional[Direction] = None):
        """
        Generates all valid positions adjacent to itself. If dir is specified, only generates positions in the appropriate direction.
        """
        assert self.in_bounds

        def adjacent_1D(x_or_y):
            for displacement in [-1, 1]:
                new_pos = x_or_y(self) + displacement
                if Pos._in_bounds(new_pos):
                    yield new_pos

        if dir is None or dir is Direction.Vertical:
            for new_row in adjacent_1D(lambda pos: pos.row):
                yield Pos(new_row, self.col)
        
        if dir is None or dir is Direction.Horizontal:
            for new_col in adjacent_1D(lambda pos: pos.col):
                yield Pos(self.row, new_col)

    def regularise(self):
        """
        Maps a position to its equivalent position in the board's top-left quadrant (Q4). Note that scrabble boards are symmetric about the central row and column
        """
        assert self.in_bounds

        if self._row > 7:
            self._row = Pos.MAX_SIZE - (self._row + 1)
        if self._col > 7:
            self._col = Pos.MAX_SIZE - (self._col + 1)
        
        return self


    @staticmethod
    def _in_bounds(x: int):
        # Scrabble boards are 15x15
        return 0 <= x < Pos.MAX_SIZE

    def __add__(self, other):
        return Pos(self.row + other.row, self.col + other.col)
    
    def __sub__(self, other):
        return Pos(self.row - other.row, self.col - other.col)
    
    def __eq__(self, other) -> bool:
        return (self.row == other.row) and (self.col == other.col)
    
    def __lt__(self, other) -> bool:
        return (self.row, self.col) < (other.row, other.col)
    
    def __hash__(self) -> int:
        return hash((self.row, self.col))

    def __repr__(self) -> str:
        return f"Pos({self._row}, {self._col})"
    
    # Convert to match Woggles omgwords position format
    # TODO: we need to swap the order of row/col depending on the orientation of the play
    def __str__(self) -> str:
        return f"{chr(ord('A') + self.col)}{self.row}"