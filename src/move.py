from typing import List
from enum import Enum

from tile import Tile
from board_pos import Pos

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

class Move:
    def __init__(self, tiles: List[Tile], coordinates: List[Pos]):
        assert len(tiles) == len(coordinates)
        assert 0 < len(tiles) <= 7

        # Sort tiles by position
        tile_positions = sorted(zip(tiles, coordinates), key=lambda tile_pos: tile_pos[1])

        self._tiles: List[Tile] = [tile_pos[0] for tile_pos in tile_positions]
        self._coordinates: List[Pos] = [tile_pos[1] for tile_pos in tile_positions]

    @property
    def is_valid(self):
        along_row = all(pos.row == self._coordinates[0].row for pos in self._coordinates)
        along_col = all(pos.col == self._coordinates[0].col for pos in self._coordinates)
        return along_row or along_col
    
    @property
    def start(self) -> Pos:
        return self._coordinates[0]
    
    @property
    def end(self) -> Pos:
        return self._coordinates[-1]
    
    @property
    def coordinates(self):
        return self._coordinates
    
    @property
    def direction(self):
        assert self.is_valid, "Should not call .direction on invalid move"

        diff = self._coordinates[-1] - self._coordinates[0]
        if diff.row == 0:
            return Direction.Horizontal
        elif diff.col == 0:
            return Direction.Vertical
        
    def __iter__(self):
        return iter(zip(self._tiles, self._coordinates))