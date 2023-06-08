from typing import List

from src.tile import Tile
from src.board_pos import Pos, Direction

class Move:
    def __init__(self, tiles: List[Tile], coordinates: List[Pos]):
        assert len(tiles) == len(coordinates)
        assert 0 < len(tiles) <= 7

        # Sort tiles by position
        tile_positions = sorted(zip(tiles, coordinates), key=lambda tile_pos: tile_pos[1])

        self._tiles: List[Tile] = [tile_pos[0] for tile_pos in tile_positions]
        self._coordinates: List[Pos] = [tile_pos[1] for tile_pos in tile_positions]

    @classmethod
    def fromstr(cls, move_str: str):
        """
        Constructs a Move based on a string in the Woogles format.
        """
        if len(move_str.split()) != 2:
            raise ValueError(f"Cannot construct move from invalid format {move_str}")
        
        start_pos_str, tiles_str = move_str.split()
        curr_pos, dir = Pos.fromstr(start_pos_str)

        tiles: List[Tile] = []
        coords: List[Pos] = []
        for letter in tiles_str:
            if letter != '.':
                tiles.append(Tile.fromstr(letter))
                coords.append(curr_pos)
            curr_pos += dir.epsilon
        
        move = cls(tiles, coords)
        assert move.is_valid
        return move

    @property
    def is_valid(self):
        along_row = all(pos.row == self._coordinates[0].row for pos in self._coordinates)
        along_col = all(pos.col == self._coordinates[0].col for pos in self._coordinates)
        unique_positions = len(set(self.coordinates)) == len(self.coordinates)
        return (along_row or along_col) and unique_positions
    
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
        
    @property
    def n_of_unset_blanks(self):
        return sum(tile.is_blank and not tile.is_set for tile in self._tiles)
        
    def set_blanks(self, blanks: str) -> bool:
        if self.n_of_unset_blanks != len(blanks):
            return False
        
        for i, blank in enumerate(self.blanks()):
            try:
                blank.set_letter(blanks[i])
            except ValueError:
                return False
            
        return True

    def blanks(self):
        for tile in self._tiles:
            if tile.is_blank:
                yield tile
        

    def format(self):
        """
        Converts a move to Woogles string format: "<start_pos> <tiles>", where '.' is used to represent playing through an existing tile.
        """
        assert self.is_valid, "Cannot display invalid move"
        move = f"{self._tiles[0].format()}"
        for i, (tile, pos) in enumerate(self)[1:]:
            distance_from_previous = (pos - self.coordinates[i - 1]).L1_norm() # Displacement should be 0 in one direction
            move += '.' * (distance_from_previous - 1) # Represents tiles being played through
            move += tile.format()

        return f"{self.start.format(self.direction)} {move}"
    
    
    def __eq__(self, other) -> bool:
        return self._tiles == other._tiles and self.coordinates == other.coordinates 

    def __iter__(self):
        return iter(zip(self._tiles, self._coordinates))
    
    # Matches Woogles format
    def __repr__(self):
        return self.format()
