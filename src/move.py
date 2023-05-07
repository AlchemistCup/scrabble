from typing import List

from tile import Tile
from board_pos import Pos

class Move:
    def __init__(self, tiles: List[Tile], coordinates: List[Pos]):
        assert len(tiles) == len(coordinates)
        assert len(tiles) > 0

        # Sort tiles by position
        tile_positions = sorted(zip(tiles, coordinates), key=lambda tile_pos: tile_pos[1])

        self._tiles: List[Tile] = [tile_pos[0] for tile_pos in tile_positions]
        self._coordinates: List[Pos] = [tile_pos[1] for tile_pos in tile_positions]

    @property
    def is_valid(self):
        along_row = all(pos[0] == self._coordinates[0][0] for pos in self._coordinates)
        along_col = all(pos[1] == self._coordinates[0][1] for pos in self._coordinates)
        return along_row or along_col
    
    @property
    def start(self) -> Pos:
        return self._coordinates[0]
    
    @property
    def end(self) -> Pos:
        return self._coordinates[-1]
    
    @property
    def is_horizontal(self):
        return all(pos[0] == self._coordinates[0][0] for pos in self._coordinates)

    def __iter__(self):
        return iter(zip(self._tiles, self._coordinates))